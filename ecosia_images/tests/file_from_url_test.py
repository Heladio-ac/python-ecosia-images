import pytest
import ecosia_search as md

## op: 2019-07-11 13:05 +w27 jue 
#@pytest.mark.skipif('DBG > 50')
@pytest.mark.parametrize('out_plan, in_plan',
    [
        ('il_fullxfull.381484942_lcyi.jpg'
            , 'https://img0.etsystatic.com/005/0/5282912/il_fullxfull.381484942_lcyi.jpg')

        , ( 'fluffy-red-cat-black-background-1080P-wallpaper.jpg'
            , 'http://www.wallpaperbetter.com/wallpaper/80/805/221/fluffy-red-cat-black-background-1080P-wallpaper.jpg')

        , ( 'Animals___Cats_Small_beautiful_red_cat_on_the_stone_044669_.jpg'
            , 'http://www.zastavki.com/pictures/originals/2013/Animals___Cats_Small_beautiful_red_cat_on_the_stone_044669_.jpg')

        , ( 'fe8f588a3470ac3884359d1c7607378f.jpg'
            , 'https://s-media-cache-ak0.pinimg.com/736x/fe/8f/58/fe8f588a3470ac3884359d1c7607378f.jpg')

        , ( 'c54580064938ea189a14b8a457228694.jpg'
        , 'https://s-media-cache-ak0.pinimg.com/736x/c5/45/80/c54580064938ea189a14b8a457228694.jpg')

        , ( 'fire-red-cat-set.jpg'
        , 'https://kittensplaypen.net/3523-thickbox_default/fire-red-cat-set.jpg')

        , ('https://lookaside.fbsbx.com/lookaside/crawler/media/?media_id=196274217061170'  ##???
        , 'https://lookaside.fbsbx.com/lookaside/crawler/media/?media_id=196274217061170')

        , ( 'Animals_Cats_Red_Cat_033474_.jpg'
        , 'http://www.zastavki.com/pictures/1920x1200/2012/Animals_Cats_Red_Cat_033474_.jpg')

        , ( 'Awesome-Red-Somali-Cat-Sitting.jpg'
        , 'https://www.askideas.com/media/26/Awesome-Red-Somali-Cat-Sitting.jpg')

        , ( 'Russian-blue-cat.jpg'
        , 'http://miriadna.com/desctopwalls/images/max/Russian-blue-cat.jpg')

        , ( '1fa511227974ad6cc10f02f0e806d4b8--russian-blue-cats-gray-cats.jpg'
        , 'https://s-media-cache-ak0.pinimg.com/736x/1f/a5/11/1fa511227974ad6cc10f02f0e806d4b8--russian-blue-cats-gray-cats.jpg')

        , ( '1280-648561826-rusian-blue-cat.jpg'
        , 'https://pixfeeds.com/images/cats/1280-648561826-rusian-blue-cat.jpg')

        , ( '57148496.jpg'
        , 'https://metrouk2.files.wordpress.com/2017/06/57148496.jpg?w=748&h=497&crop=1')

        , ( '89f99f5f732c23aea4a2220f70e73231.jpg'
        , 'https://www.pets4homes.co.uk/images/breeds/25/large/89f99f5f732c23aea4a2220f70e73231.jpg')

        , ( 'fun-facts-about-russian-blue-cats.jpg'
        , 'https://www.aspcapetinsurance.com/media/2376/fun-facts-about-russian-blue-cats.jpg')

        , ( 'wallpaper.1000webgames-com-Russian-Blue.jpg'
        , 'http://www.exploretalent.com/articles/wp-content/uploads/2014/10/wallpaper.1000webgames-com-Russian-Blue.jpg')

        , ( 'russianbluehed.png'
        , 'https://images.mentalfloss.com/sites/default/files/styles/mf_image_16x9/public/russianbluehed.png?itok=3dlglcvn&resize=1100x1100')

        , ( '681b66d8f111dacade9f1f26b4440ce9.jpg'
        , 'https://i.pinimg.com/originals/68/1b/66/681b66d8f111dacade9f1f26b4440ce9.jpg')
        , ('AVtb1nB0wJQ/maxresdefault.jpg'
        , 'https://i.ytimg.com/vi/AVtb1nB0wJQ/maxresdefault.jpg')

        , ( 'poLfp3twzMs/maxresdefault.jpg'
        , 'https://i.ytimg.com/vi/poLfp3twzMs/maxresdefault.jpg')

        , ( 'green-cat-5.jpg'
        , 'http://boredomtherapy.com/wp-content/uploads/2014/12/green-cat-5.jpg')

        , ( 'green-dragon-cat-bumblebee-dog-pets-different-looks-russia.jpg'
        , 'https://data1.ibtimes.co.in/en/full/537290/green-dragon-cat-bumblebee-dog-pets-different-looks-russia.jpg')

        , ( 'Green-caterpillar-WA.jpg'
        , 'https://upload.wikimedia.org/wikipedia/commons/8/88/Green-caterpillar-WA.jpg')

        , ( 'greencats02.jpg'
        , 'http://4.bp.blogspot.com/_vbS7BIUoZ94/TQj_NaAtLmI/AAAAAAAAB2Y/7YQjMASazXI/s1600/greencats02.jpg')

        , ( '172536.jpg'
        , 'https://cdn.images.dailystar.co.uk/dynamic/1/photos/536000/936x622/172536.jpg')

        , ( 'Bulgaria-green-cat.jpg'
        , 'http://www.bellenews.com/wp-content/uploads/2014/12/Bulgaria-green-cat.jpg')

        , ( '2400146700000578-2871954-image-a-43_1418413395821.jpg'
        , 'http://i.dailymail.co.uk/i/pix/2014/12/12/2400146700000578-2871954-image-a-43_1418413395821.jpg')
    ])
def test_url_like_from_phrase(out_plan, in_plan):
    assert out_plan == md.url_like_from_phrase(in_plan)
    # def url_like_from_phrase(phrase: str, pre: str='', post: str='') -> str:



