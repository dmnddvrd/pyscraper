from scrapy_proxy_pool.policy import BanDetectionPolicy

# This policy has been created due to Getting "AttributeError('Response content isn't a text')"


class BanDetectionPolicyNotText(BanDetectionPolicy):
    def response_is_ban(self, request, response):
        # Following line causes errors
        # if self.BANNED_PATTERN.search(response.text):
        #    return True
        if response.status not in self.NOT_BAN_STATUSES:
            return True
        if response.status == 200 and not len(response.body):
            return True
