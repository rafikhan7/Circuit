#!/usr/bin/env python3

import json
import webbrowser
import secrets
from os import environ
from urllib.request import Request, urlopen
from urllib.parse import urlencode, urlparse, parse_qs
from pprint import pprint


def openid_discovery():
    """Perform OpenID Discovery

    SciStarter supports OpenID Connect Discovery, so there is a
    standardized, machine readable description of our OpendID/OAuth
    configuration which can be retrieved at any time.

    Normally, there is no need to perform discovery very often. Just
    cache the results.

    """

    r = urlopen("https://scistarter.org/.well-known/openid-configuration")

    if r.status != 200:
        raise Exception(r.status, r.reason)

    return json.loads(r.read())


def authorize(config):
    """Perform the OAuth flow to retrieve an access token

    Authorization in OpenID Connect is via OAuth 2.

    """

    # If we were writing a server-side request handler, it would be a
    # good idea to save the URL for the next page the user expects to
    # see at this time. Usually, we would store it in the session.
    # Then, once the authorization was complete, it would be easy to
    # forward user to where they expected to go.

    # This is a nonce which has no purpose or meaning except to make
    # it impossible for a hostile middleman to replay the request. The
    # state, too, should be saved in the session so as to accessible
    # later in the process.
    state = secrets.token_hex(16)

    # Normally we would be doing this in a server-side HTTP request
    # handler rather than in a standalone program, in which case we
    # would simply return a redirect response rather than messing
    # about with the webbrowser module.
    webbrowser.open_new_tab(
        config["authorization_endpoint"]
        + "?"
        + urlencode(
            {
                # The client_id is provided by SciStarter, email us at
                # info@scistarter.org to get one.
                "client_id": "418316",
                "response_type": "code",
                # Requesting the openid scope is a protocol requirement
                # Requesting the profile scope gives us read access to
                # basic user information, if the user grants it.
                # Requesting the participation scope gives us the
                # right to add participation events to the user's
                # record, if the user grants it.
                "scope": "openid profile participation",
                "state": state,
                "redirect_uri":
                # This URL would never be the one you really use.
                # Instead, you will have provided one or more URLs on
                # your own domain to us when you requested a
                # client_id. The redirect_uri parameter must be one of
                # those URLs.
                "https://example.com/openid/scistarter",
            }
        )
    )

    # Once the user has granted permissions, scistarter will redirect
    # the user to the specified redirect_uri. That would result in
    # another request handler on your server processing that request to
    # complete the authorization. Since we're not in a server here, we
    # do this instead:
    redirected_to = input(
        "Please perform the authorization in your browser, then copy and paste the URL you get redirected to here: "
    )
    params = parse_qs(urlparse(redirected_to).query)

    try:
        code = params["code"][0]
    except (KeyError, IndexError):
        raise Exception("No authorization code was provided")

    # Now that the user has identified themself to SciStarter and
    # granted permissions, we have to identify ourself as the rightful
    # recipient of those permissions and retrieve an access token.

    req = Request(
        method="POST",
        url=config["token_endpoint"],
        data=urlencode(
            {
                "client_id": "418316",
                "client_secret": "dbccade1d890b729952ec3b0b0abd69abd4ae55af4da5763b216da29",
                # redirect_uri must match the redirect_uri used above
                "redirect_uri": "https://example.com/openid/scistarter",
                "grant_type": "authorization_code",
                "code": code,
                "state": state,
            }
        ).encode("utf8"),
    )

    r = urlopen(req)

    if r.status != 200:
        raise Exception(r.status, r.reason)

    authorization = json.loads(r.read())

    # Now we have an access token, which will be good for several
    # hours and which will allow us to access SciStarter on the user's
    # behalf.
    access_token = authorization["access_token"]

    # We also have a refresh token, which can be used to retrieve a
    # new access token after the current one expires, as long as the
    # user does not have it revoked.
    refresh_token = authorization["refresh_token"]

    return access_token, refresh_token


def refresh(config, refresh_token):
    """Retrieve a new access token, given a refresh token

    Access tokens expire after a time. Refresh tokens don't expire
    until they are used or revoked. For use cases where you're not
    using OpenID Connect as your primary way of authenticating the
    user, it's quite possible for the user to come back to your site
    and authenticate through other means long after the access token
    is no longer valid. When this happens, you can use the refresh
    token to renew your access to SciStarter, without interrupting the
    user to ask for permissions that you have already been granted.

    Refresh tokens should never leave your server, except to be sent
    to ours over an encrypted connection.

    SciStarter's refresh tokens are single use. Using a refresh token
    consumes it, and issues a new one along with an access token.

    """

    req = Request(
        method="POST",
        url=config["token_endpoint"],
        data=urlencode(
            {
                "client_id": "418316",
                "client_secret": "dbccade1d890b729952ec3b0b0abd69abd4ae55af4da5763b216da29",
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
            }
        ).encode("utf8"),
    )

    r = urlopen(req)

    if r.status != 200:
        raise Exception(r.status, r.reason)

    authorization = json.loads(r.read())

    return authorization['access_token'], authorization['refresh_token']


def get_profile(config, token):

    """Retrieve user information

    In the process of granting the token, the user was prompted to
    allow (or deny) us access to their information. The specific
    information depends on the scopes we requested, but whatever
    information they allowed is available via the userinfo endpoint.

    If participation API access was granted, the
    'participation_api_granted' field in the return value will be
    true.

    It's not necessary to retrieve the profile information every time
    you are authorized. Once is usually sufficient.

    """

    req = Request(
        method="GET",
        url=config["userinfo_endpoint"],
        # Any request that is authorized by the token should have this
        # Authorization HTTP header
        headers={"Authorization": "Bearer " + token},
    )

    r = urlopen(req)

    if r.status != 200:
        raise Exception(r.status, r.reason)

    return json.loads(r.read())


def record_participation(config, token, project_slug=None):
    """Record a participation event for the user

    This will only work if the participation scope is available, which
    means that the user specifically granted permission to share
    information with SciStarter.

    There are two variations on this process: if we only have one
    project associated with the client_id, all we need is our token.
    On the other hand, if have more than one project for the same
    client_id, we also need to provide the slug which identifies the
    specific project that the user participated in.

    The project_slug parameter should contain the textual unique
    identifier of the project. It is easily accesible from the project
    URL. In the URL https://scistarter.org/airborne-walrus-capture the
    slug is the string airborne-walrus-capture

    """

    if project_slug is None:
        endpoint = "https://scistarter.org/api/participation/openid"
    else:
        endpoint = "https://scistarter.org/api/participation/openid/" + project_slug

    req = Request(
        method="POST",
        url=endpoint,
        headers={"Authorization": "Bearer " + token},
        data=urlencode(
            {
                "type": "classification",  # other options: 'collection', 'signup'
                "duration": 31,  # Seconds the user spent participating, or an estimate
            }
        ).encode("utf8"),
    )

    r = urlopen(req)

    if r.status != 200:
        raise Exception(r.status, r.reason)

    return json.loads(r.read())


if __name__ == "__main__":
    config = openid_discovery()

    # print("CONFIG")
    # print(config)

    access_token, refresh_token = authorize(config)

    print("REFRESH_TOKEN")
    print(refresh_token)

    # We don't need to do this at this time, except to demonstrate
    # how. The current access token is valid, since we just retrieved
    # it, and does not need to be refreshed.
    access_token, refresh_token = refresh(config, refresh_token)

    print("ACCESS TOKEN")
    pprint(access_token)

    profile = get_profile(config, access_token)

    print("PROFILE")
    pprint(profile)

    # result = record_participation(config, access_token)

    # print("RESULT")
    # pprint(result)