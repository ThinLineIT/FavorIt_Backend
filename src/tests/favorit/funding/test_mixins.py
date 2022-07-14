from favorit.favorit_user.models import FavorItUser
from favorit.funding.models import Funding, Product


class TestFundingMixins:
    def create_funding(self):
        product = Product.objects.create(link="testlink", price=1000, option="some options")
        maker = FavorItUser.objects.create(kakao_user_id="12345")
        funding = Funding.objects.create(
            maker=maker, product=product, name="some funding", contents="some contents", due_date="2022-01-01"
        )
        return product, maker, funding
