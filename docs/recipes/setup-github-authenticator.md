# Authenticate using GitHub Usernames

The GitHub Authenticator lets users log into your JupyterHub using their GitHub user ID/password.
To do so, you’ll first need to register an application with GitHub,
and then provide information about this application to JupyterHub configuration
([`jupyterhub_config.py`](../../jupyterhub/jupyterhub_config.py))

> _Note_: You’ll need a GitHub account in order to complete these steps.

## Step 1: Create a GitHub application

1. Go to the [GitHub OAuth app creation page](https://github.com/settings/apps/new).

    - _Application name_: Choose a descriptive application name (e.g. `medialab`)
    - _Homepage URL_: Use the IP address or URL of your JupyterHub. e.g. `http(s)://<my-medialab-url>`.
    - _Application description_: Use any description that you like.
    - *Authorization callback UR*L: Insert text with the following form:
      `http(s)://<my-medialab-url>/hub/oauth_callback`

<p align="center">
  <img width="536" height="516" alt="Create a GitHub OAuth application" src="https://tljh.jupyter.org/en/latest/_images/create_application.png">
</p>

2. Click “Register application”. You’ll be taken to a page with the registered application details.

3. Copy the `Client ID` and `Client Secret` from the application details page.
   You will use these later to configure your JupyterHub authenticator.

## Step 2: Configure JupyterHub to use the GitHub Oauthenticator

1. Replace `jupyterhub-dummyauthenticator` with
   `oauthenticator` in the list of dependancies of JupyterHub [`requirements.txt`](../../jupyterhub/requirements.txt)

```txt
# ./jupyterhub/requirements.txt#L2
oauthenticator
```

2. Set callback URL, client ID, and client secret in JupyterHub configuration
   ([`jupyterhub_config.py`](../../jupyterhub/jupyterhub_config.py))

```python
# ./jupyterhub/jupyterhub_config.py#L11

## Authenticator
from oauthenticator.github import GitHubOAuthenticator
c.JupyterHub.authenticator_class = GitHubOAuthenticator

c.GithubOAuthenticator.oauth_callback_url = 'http(s)://<my-medialab-url>/hub/oauth_callback'
c.GithubOAuthenticator.client_id = 'Client ID'
c.GithubOAuthenticator.client_secret = 'Client Secret'
```

Additionally, you can specify usernames to whitelist and/or usernames to designate as admins.

```python
c.GithubOAuthenticator.allowed_users = {'good-user_1', 'good-user_2'}
c.GithubOAuthenticator.admin_users = {'admin-user_0'}
```

4. Finally, rebuild the custom JupyterHub Docker image.

```bash
docker-compose build jupyterhub
```

## Step 3: Confirm that the new authenticator works

1. Open an incognito window in your browser (do not log out until you confirm that the new authentication method works!)
2. Go to your JupyterHub URL.
3. You should see a GitHub login button like below:

<p align="center">
  <img width="545" height="309" alt="The GitHub authenticator login button" src="https://tljh.jupyter.org/en/latest/_images/login_button.png">
</p>

4. After you log in with your GitHub credentials, you should be directed to the Jupyter interface used in this JupyterHub.

## Resources

-   [OAuthenticator docs: Get started](https://oauthenticator.readthedocs.io/en/latest/getting-started.html#installation)
-   [JupyterHub docs: GitHub Setup](https://oauthenticator.readthedocs.io/en/latest/getting-started.html#github-setup)
-   [JupyterHub docs: Configure GitHub OAuth](https://jupyterhub.readthedocs.io/en/latest/reference/config-ghoauth.html)
-   [The Little JupyterHub: How to Guides](https://tljh.jupyter.org/en/latest/howto/auth/github.html)
