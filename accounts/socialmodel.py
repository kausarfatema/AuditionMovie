class SocialLogin(object):
    """
    Represents a social user that is in the process of being logged
    in. This consists of the following information:
    `account` (`SocialAccount` instance): The social account being
    logged in. Providers are not responsible for checking whether or
    not an account already exists or not. Therefore, a provider
    typically creates a new (unsaved) `SocialAccount` instance. The
    `User` instance pointed to by the account (`account.user`) may be
    prefilled by the provider for use as a starting point later on
    during the signup process.
    `token` (`SocialToken` instance): An optional access token token
    that results from performing a successful authentication
    handshake.
    `state` (`dict`): The state to be preserved during the
    authentication handshake. Note that this state may end up in the
    url -- do not put any secrets in here. It currently only contains
    the url to redirect to after login.
    `email_addresses` (list of `EmailAddress`): Optional list of
    e-mail addresses retrieved from the provider.
    """

    def __init__(self, user=None, account=None, token=None, email_addresses=[]):
        if token:
            assert token.account is None or token.account == account
        self.token = token
        self.user = user
        self.account = account
        self.email_addresses = email_addresses
        self.state = {}

    def connect(self, request, user):
        self.user = user
        self.save(request, connect=True)

    def serialize(self):
        serialize_instance = get_adapter().serialize_instance
        ret = dict(
            account=serialize_instance(self.account),
            user=serialize_instance(self.user),
            state=self.state,
            email_addresses=[serialize_instance(ea) for ea in self.email_addresses],
        )
        if self.token:
            ret["token"] = serialize_instance(self.token)
        return ret

    @classmethod
    def deserialize(cls, data):
        deserialize_instance = get_adapter().deserialize_instance
        account = deserialize_instance(SocialAccount, data["account"])
        user = deserialize_instance(get_user_model(), data["user"])
        if "token" in data:
            token = deserialize_instance(SocialToken, data["token"])
        else:
            token = None
        email_addresses = []
        for ea in data["email_addresses"]:
            email_address = deserialize_instance(EmailAddress, ea)
            email_addresses.append(email_address)
        ret = cls()
        ret.token = token
        ret.account = account
        ret.user = user
        ret.email_addresses = email_addresses
        ret.state = data["state"]
        return ret

    def save(self, request, connect=False):
        """
        Saves a new account. Note that while the account is new,
        the user may be an existing one (when connecting accounts)
        """
        assert not self.is_existing
        user = self.user
        user.save()
        self.account.user = user
        self.account.save()
        if app_settings.STORE_TOKENS and self.token and self.token.app_id:
            self.token.account = self.account
            self.token.save()
        if connect:
            # TODO: Add any new email addresses automatically?
            pass
        else:
            setup_user_email(request, user, self.email_addresses)

    @property
    def is_existing(self):
        """
        Account is temporary, not yet backed by a database record.
        """
        return self.account.pk is not None

    def lookup(self):
        """
        Lookup existing account, if any.
        """
        assert not self.is_existing
        try:
            a = SocialAccount.objects.get(
                provider=self.account.provider, uid=self.account.uid
            )
            # Update account
            a.extra_data = self.account.extra_data
            self.account = a
            self.user = self.account.user
            a.save()
            # Update token
            if app_settings.STORE_TOKENS and self.token and self.token.app.pk:
                assert not self.token.pk
                try:
                    t = SocialToken.objects.get(
                        account=self.account, app=self.token.app
                    )
                    t.token = self.token.token
                    if self.token.token_secret:
                        # only update the refresh token if we got one
                        # many oauth2 providers do not resend the refresh token
                        t.token_secret = self.token.token_secret
                    t.expires_at = self.token.expires_at
                    t.save()
                    self.token = t
                except SocialToken.DoesNotExist:
                    self.token.account = a
                    self.token.save()
        except SocialAccount.DoesNotExist:
            pass

    def get_redirect_url(self, request):
        url = self.state.get("next")
        return url

    @classmethod
    def state_from_request(cls, request):
        state = {}
        next_url = get_next_redirect_url(request)
        if next_url:
            state["next"] = next_url
        state["process"] = get_request_param(request, "process", "login")
        state["scope"] = get_request_param(request, "scope", "")
        state["auth_params"] = get_request_param(request, "auth_params", "")
        return state

    @classmethod
    def stash_state(cls, request):
        state = cls.state_from_request(request)
        verifier = get_random_string(12)
        request.session["socialaccount_state"] = (state, verifier)
        return verifier

    @classmethod
    def unstash_state(cls, request):
        if "socialaccount_state" not in request.session:
            raise PermissionDenied()
        state, verifier = request.session.pop("socialaccount_state")
        return state

    @classmethod
    def verify_and_unstash_state(cls, request, verifier):
        if "socialaccount_state" not in request.session:
            raise PermissionDenied()
        state, verifier2 = request.session.pop("socialaccount_state")
        if verifier != verifier2:
            raise PermissionDenied()
        return state