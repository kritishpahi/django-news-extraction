from django.shortcuts import render, render_to_response
from django.views.generic.list import ListView

from news_ie.extraction.vehicle_no import vehicle_no
from news_ie.models import News
from news_ie.views import extract_items, similar_story
from rss.get_news import (get_data_from_rss, get_rss_republica, rss,
                          testaccidentnews)
from rssdb.models import rssdata


def index(request):

    # from RSS feed get news list
    news_list = get_data_from_rss()
    # republic_list = get_rss_republica()
    # print(republic_list)
    newss = []
    repnews = []
    getnews = []

    getdata = rssdata()
    # news_body
    for news in news_list:
        # print(news)
        newss.append(str(news))
    # import ipdb
    # ipdb.set_trace()

    # for news in republic_list:
    #     repnews.append(str(news))
    # print(len(repnews))

    # newss = [str(news[0]) for news in news_list]

    # newss +=repnews
    print("lenght of news:")
    print(len(newss))
    # headings
    headings = [post.title for post in rss.entries]
    print("heading no", len(headings))
    # indexes = []
    # newheadings=[]
    # newsindex = []
    # # print(len(headings))
    # #test accident news
    # for i in headings:
    #     test = testaccidentnews(i)
    #     # print(i,test)
    #     if test == False:
    #         indexes.append(headings.index(i))
    #         # del headings[headings.index(i)]
    #     else:
    #         newheadings.append(i)
    #         newsindex.append(headings.index(i))
    # print("head",len(newheadings))
    # print(indexes)
    # newss = [v for i, v in enumerate(newss) if i not in indexes]
    # getnews = [v for i, v in enumerate(newss) if i in newsindex]
    # print("news",len(newss))
    # print(newss)
    # links
    links = [post.link for post in rss.entries]
    # linkss = [v for i, v in enumerate(links) if i in newsindex]
    # print(linkss)

    # combine the news headings and news body
    detailNews = dict(zip(headings, newss))
    dictnews = dict(zip(newss, headings))
    # combine headings and links
    newsLinks = dict(zip(headings, links))

    # all news form db
    allNews = News.objects.all()

    allIndex = []
    newsStory = []

    for i, n in enumerate(newss):
        # getdata = rssdata()
        similarCoeff = []

        for dbNews in allNews:
            coeff = similar_story(n, dbNews.body)
            similarCoeff.append(coeff)

        if max(similarCoeff) > 0.60:
            print("Similary Story exists at index: ")
            newsIndex = similarCoeff.index(max(similarCoeff))
            print(newsIndex)
            story = allNews[newsIndex]
            newsStory.append(story)

            # allIndex.append(newsIndex)
            # newsStory = allNews[newsIndex]
            # print(newsStory.location)

        else:
            print("Extraction Requires")
            print("Extracting:")
            story = extract_items(n)
            getdata.day = story.day
            getdata.date = story.date
            getdata.body = story.body
            getdata.vehicle_no = story.vehicle_no
            getdata.death_no = story.death_no
            getdata.injury = story.injury
            getdata.death = story.death
            getdata.location = story.location
            # getdata.header = dictnews[n]

            getdata.header = headings[i]
            getdata.slug = story.slug

            newsStory.append(story)
            print("Extracting complete:")
            # save_storye(getdata,n)
            getdata.save()
            print("Save Complete for RSS")

    # This line is main
    headingDetail = dict(zip(headings, newsStory))

    return render_to_response('rssdb/index.html', {
        'detailnews': detailNews,
        'newslinks': newsLinks,
        'newsstory': newsStory,
        'headingdetail': headingDetail,
    })

#
# def save_storye(story, data):
#     sim = []
#     # getdata = rssdata()
#     # get all the saved story
#     savedStory = rssdata.objects.all()
#     for s in savedStory:
#         doc2 = set(s.body.split())
#         coefficient = similar_story(data, s.body)
#         sim.append(coefficient)
#
#     # print(sim)
#     jacc_max = max(sim)
#     # print(jacc_max)
#
#     # set the threshold value to identify Duplicate
#
#     thresHold = .90
#
#     if jacc_max < thresHold:
#
#         s = story.save()
#
#         print("Save Successful:")
#     else:
#         print("Duplicate News Exists:")
