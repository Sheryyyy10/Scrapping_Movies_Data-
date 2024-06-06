import concurrent
import urllib
from concurrent.futures import ThreadPoolExecutor
from .models import AppData, Language, Country
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
import threading
from rest_framework.response import Response
from rest_framework.views import APIView
from requests_html import HTMLSession, Element
from datetime import datetime
from requests_html import HTMLSession
from django.http import JsonResponse
from API.functions import *
import concurrent.futures


class imdb(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            movie_name = request.GET.get('movie_name')
            if not movie_name:
                return JsonResponse({"error": "Movie name not provided"})

            # Search for the movie on Rotten Tomatoes
            sess = HTMLSession()
            rotten_search_url = f"https://www.rottentomatoes.com/search?search={movie_name}"
            rotten_search_response = sess.get(rotten_search_url)


            # Extracting movie title from search results
            title_element = rotten_search_response.html.find('.movieTitle a')
            if not title_element:
                return JsonResponse({"error": "Movie not found on Rotten Tomatoes"})

            movie_title = title_element[0].text.strip()

            # Scrape reviews from IMDb based on the movie title
            imdb_reviews_url = f"https://www.imdb.com/title/{movie_title}/reviews"
            imdb_reviews_response = sess.get(imdb_reviews_url)

            # Extracting reviews
            reviews_selector = '#main > section > div.lister > div.lister-list > div'
            reviews_elements = imdb_reviews_response.html.find(reviews_selector)
            reviews_data = []

            for review_element in reviews_elements:
                # Extracting username
                username_element = review_element.find('span.display-name-link > a')
                username = username_element[0].text.strip() if username_element else None

                # Extracting post date
                postdate_element = review_element.find('span.review-date')
                postdate = postdate_element[0].text.strip() if postdate_element else None

                # Extracting comment text
                comment_element = review_element.find('div.content > div.text.show-more__control')
                comment = comment_element[0].text.strip() if comment_element else None

                reviews_data.append({
                    "userName": username,
                    "postdate": postdate,
                    "comment": comment
                })

            return JsonResponse(reviews_data, safe=False)

        except Exception as e:
            return JsonResponse({"error": f"An error occurred: {e}"})


# class rotten(APIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

from requests_html import HTMLSession
import time


def rotten(request):
    global rating, revenue, producer, photo_urls, cast_data, reviews_data
    try:
        # Start timer
        t1 = time.perf_counter()

        movie_name = request.GET['movie_name']
        sess = HTMLSession()
        url = f"https://www.rottentomatoes.com/search?search={movie_name.replace(' ', '_')}"
        response = sess.get(url)

        # Extracting the first search result URL
        rating_page_url = '#search-results > search-page-result:nth-child(2) > ul > search-page-media-row:nth-child(1) > a:nth-child(2)'
        rating_page_url_element = response.html.find(rating_page_url)
        if rating_page_url_element:
            relative_url = rating_page_url_element[0].attrs['href']
            rating_page_url = relative_url
            sess = HTMLSession()
            url = rating_page_url
            response = sess.get(url)

            # Extracting ratings
            rotten_rating_selector = '#modules-wrap > div.media-scorecard.no-border > media-scorecard > rt-button:nth-child(3) > rt-text'
            rotten_rating_element = response.html.find(rotten_rating_selector, first=True)

            if rotten_rating_element:
                rating = rotten_rating_element.text.strip()
                rating = rating + '%' if rating else ''
            else:
                rating = None

            # Extracting revenue
            revenue_element = ['#info li:contains("Box Office (Gross USA):")']
            for path in revenue_element:
                try:
                    revenue = response.html.find(path)
                    if revenue:
                        revenue = revenue[0].text
                        revenue = revenue.replace('Box Office (Gross USA):', '').strip()
                    else:
                        revenue = None
                except Exception as e:
                    revenue = None

            # Extracting producer
            producer_element = ['.category-wrap']
            for path in producer_element:
                try:
                    producer_info = response.html.find(path)
                    if producer_info:
                        producer = producer_info[1].text.replace('Producer: ', '').strip()
                except Exception as e:
                    producer = None

            where_to_watch_elements = response.html.find('where-to-watch-meta')
            where_to_watch_info = {}

            for where_to_watch_element in where_to_watch_elements:
                link = where_to_watch_element.attrs.get('href', None)
                if link:
                    if 'netflix' in link.lower():
                        where_to_watch_info['netflix'] = link
                    elif 'hulu' in link.lower():
                        where_to_watch_info['hulu'] = link
                    elif 'amazon' in link.lower():
                        where_to_watch_info['prime_video'] = link
                else:
                    link = "null"

            # Extracting photos URLs
            photos_elements = response.html.find('tile-photo')

            # Initialize an empty list to store photo URLs
            photo_urls = []

            # Loop through each photo element
            for photo_element in photos_elements:
                # Extract the src attribute (URL) of the image
                src = photo_element.attrs.get('image')

                # If src attribute exists, append it to the list
                if src:
                    photo_urls.append(src)

            # Check if any photo URLs were found
            if photo_urls:
                pass
            else:
                photo_urls = None

            # Extracting reviews
            reviews_url = f"{url}/reviews"
            reviews_response = sess.get(reviews_url)
            reviews_selector = '#reviews > div.review_table > div'
            reviews_elements = reviews_response.html.find(reviews_selector)
            reviews_data = []

            for review_element in reviews_elements:
                # Extracting username
                username_element = review_element.find('div.review-data > div > a.display-name')
                username = username_element[0].text.strip() if username_element else None

                # Extracting post date
                postdate_element = review_element.find('div.review-text-container > p.original-score-and-url > span')
                postdate = postdate_element[0].text.strip() if postdate_element else None

                # Extracting comment text
                comment_element = review_element.find('div.review-text-container > p.review-text')
                comment = comment_element[0].text.strip() if comment_element else None

                reviews_data.append({
                    "username": username,
                    "postdate": postdate.split(',')[0],
                    "comment": comment
                })

            # If no reviews found, set reviews_data to None
            if not reviews_data:
                reviews_data = None

            # Extracting cast data
            main_selector = '.cast-and-crew'
            main_element = response.html.find(main_selector, first=True)

            cast_data = []

            if (main_element):
                # Extracting actor names and profiles
                actor_name_elements = main_element.find('drawer-more > div > a > tile-dynamic > div > p.name')
                actor_profile_elements = main_element.find('drawer-more > div > a > tile-dynamic > rt-img')

                # Loop through each actor name and profile element
                for actor_name_element, actor_profile_element in zip(actor_name_elements, actor_profile_elements):
                    actor_name = actor_name_element.text.strip()
                    actor_profile = actor_profile_element.attrs['src']
                    cast_data.append({"actorname": actor_name, "actorprofile": actor_profile})

            # Extracting news data
            selector = '.news-and-guides'
            try:
                # Find the section with the class name "news-and-guides"
                section = response.html.find(selector, first=True)

                news_data = []

                # Find all anchor tags within the section
                anchor_tags = section.find('a')

                # Extract title, link, and thumbnail from each anchor tag
                for anchor in anchor_tags:
                    link = anchor.attrs.get('href', None)
                    thumbnail_element = anchor.find('tile-dynamic > rt-img', first=True)
                    thumbnail_link = thumbnail_element.attrs.get('src', None) if thumbnail_element else None

                    title = anchor.text.strip()

                    # Append the data to the list if title and link are not empty
                    if title and link:
                        news_data.append({
                            "title": title,
                            "news_link": link,
                            "news_thumbnail": thumbnail_link
                        })

            except Exception as e:
                # Handle exceptions
                news_data = None

            # Extracting similar movies data
            selector = '#modules-wrap > div:nth-child(10) > section'
            try:
                # Find all tile-poster-card elements within the specified selector
                poster_cards = response.html.find(selector)

                movies_data = []

                # Iterate over each poster card and extract movie details
                for card in poster_cards:
                    try:
                        title_selector = '#modules-wrap > div:nth-child(10) > section > div.content-wrap > carousel-slider > tile-poster-card:nth-child(2) > rt-link'
                        title_element = response.html.find(title_selector, first=True)
                        title = title_element.text if title_element else None

                        # Extract thumbnail
                        thumbnail_selector = 'rt-img'
                        thumbnail_element = card.find(thumbnail_selector, first=True)
                        thumbnail = thumbnail_element.attrs.get('src', None) if thumbnail_element else None

                        # Extract rotten rating
                        rotten_rating_selector = 'rt-text:nth-child(3)'
                        rotten_rating_element = card.find(rotten_rating_selector, first=True)
                        rotten_rating = rotten_rating_element.text.strip() if rotten_rating_element else None

                        # Extract audience score
                        audience_score_selector = 'rt-text:nth-child(5)'
                        audience_score_element = card.find(audience_score_selector, first=True)
                        audience_score = audience_score_element.text.strip() if audience_score_element else None

                        # Append movie data to the list
                        movies_data.append({
                            "title": title,
                            "thumbnail": thumbnail,
                            "rotten_rating": rotten_rating,
                            "audience_score": audience_score
                        })
                    except Exception as e:
                        print("An error occurred while processing a movie card:", e)

            except Exception as e:
                print("An error occurred while fetching poster cards:", e)
                movies_data = None

            rotten_data = {
                "rating": rating,
                "revenue": revenue,
                "producer": producer,
                "photos": photo_urls,
                "casts": cast_data,
                "more_like_this": movies_data,
                "news": news_data,
                "reviews": reviews_data,
                "where_to_watch": where_to_watch_info,
            }

            # Stop timer
            t2 = time.perf_counter()
            elapsed_time = t2 - t1
            print(f"Elapsed time: {elapsed_time} seconds")

            return rotten_data

        else:
            print("rating_page_url_element not found.")

    except Exception as e:
        return JsonResponse({"error": f"An error occurred in rotten: {e}"})


import time
from concurrent.futures import ThreadPoolExecutor
from django.http import JsonResponse
from requests_html import HTMLSession

import time
from concurrent.futures import ThreadPoolExecutor
from requests_html import HTMLSession
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist


class scrape_main(APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.method == 'GET':
            start_time = time.perf_counter()  # Start time measurement

            global country, language, genre, cast, synopsis, trailer, language_instance, country_instance

            try:
                with ThreadPoolExecutor(max_workers=5) as executor:
                    rotten_rating = executor.submit(rotten, request)
                    rotten_data = rotten_rating.result()

                movie_name = request.GET.get('movie_name', '')
                trakt_url = f'https://trakt.tv/search/?query={movie_name}'

                with HTMLSession() as sess:
                    response = sess.get(trakt_url)
                    response.raise_for_status()  # Ensure the request was successful

                    rating_page_url = 'body > div.frame-wrapper > div.frame.all > div > div > div:nth-child(1) > div.fanart.poster.stock-titles > a:nth-child(3)'
                    rating_page_url_element = response.html.find(rating_page_url, first=True)
                    if not rating_page_url_element:
                        return JsonResponse({"status": "success", "message": "No Movie found", "data": None},
                                            safe=False, content_type="application/json")

                    relative_url = rating_page_url_element.attrs['href']
                    rating_page_url = f"https://trakt.tv{relative_url}"
                    response = sess.get(rating_page_url)
                    response.raise_for_status()  # Ensure the request was successful

                    # Extracting the necessary details in parallel
                    with ThreadPoolExecutor(max_workers=10) as executor:
                        name_future = executor.submit(self.extract_text, response,
                                                      '#summary-wrapper > div.container.summary > div > div > div.col-md-10.col-md-offset-2.col-sm-9.col-sm-offset-3.mobile-title > h1')
                        release_future = executor.submit(self.extract_text, response,
                                                         '#overview > div.row > div.col-lg-8.col-md-7 > ul > li:nth-child(3) > span')
                        rating_future = executor.submit(self.extract_text, response,
                                                        '#summary-ratings-wrapper > div > div > div > ul.ratings > li.trakt-rating > a > div.number > div.rating')
                        poster_future = executor.submit(self.extract_attr, response, '.poster.with-overflow > img.real',
                                                        'data-original', 1)
                        audience_future = executor.submit(self.extract_text, response,
                                                          '#summary-ratings-wrapper > div > div > div > ul.stats > li:nth-child(1) > div > div.rating')
                        trailer_future = executor.submit(self.extract_attr, response,
                                                         '#overview > div.row > div.col-lg-8.col-md-7 > div.affiliate-links > div:nth-child(2) a',
                                                         'href', 0)
                        language_future = executor.submit(self.extract_language_country, response, [
                            '#overview > div.row > div.col-lg-8.col-md-7 > ul > li:contains("Language")'], 'Language',
                                                          Language)
                        duration_future = executor.submit(self.extract_text_strip, response,
                                                          '#overview > div.row > div.col-lg-8.col-md-7 > ul > li:contains("Runtime")',
                                                          'Runtime')
                        status_future = executor.submit(self.extract_text, response,
                                                        '#overview > div.row > div.col-lg-8.col-md-7 > ul > li:nth-child(3) > span')
                        country_future = executor.submit(self.extract_language_country, response, [
                            '#overview > div.row > div.col-lg-8.col-md-7 > ul > li:contains("Country")'], 'Country',
                                                         Country)
                        genre_future = executor.submit(self.extract_text_strip, response,
                                                       '#overview > div.row > div.col-lg-8.col-md-7 > ul > li:contains("Genres")',
                                                       'Genres')
                        cast_future = executor.submit(self.extract_text, response, '#cast-actors-tab > h3 > div')
                        synopsis_future = executor.submit(self.extract_text, response, '#overview')

                        name = name_future.result()
                        release = release_future.result()
                        rating = rating_future.result()
                        poster = poster_future.result()
                        audience = audience_future.result()
                        trailer_link = trailer_future.result()
                        language, language_instance = language_future.result()
                        duration = duration_future.result()
                        status = status_future.result()
                        country, country_instance = country_future.result()
                        genre = genre_future.result()
                        cast = cast_future.result()
                        synopsis = synopsis_future.result()

                        Approval_status = "Rated (R)"
                        Film_Studio = "Paramount"
                        budget_list = ['$9,500,000']
                        approx_budget = ', '.join(budget_list)

                        data = {
                            'name': name,
                            'release_year': release,
                            'imdb_rating': rating,
                            'trailer': trailer_link,
                            'poster': poster,
                            'rotten_rating': rotten_data['rating'],
                            'audience': audience,
                            'language': language_instance,
                            'duration': duration,
                            'status_released': status,
                            'season_movie': 'season' if 'shows' in relative_url else 'movie',
                            'casts': rotten_data['casts'],
                            'reviews': rotten_data['reviews'],
                            'country': country_instance,
                            'genre': genre,
                            "where_to_watch": rotten_data['where_to_watch'],
                            'approval_status': Approval_status,
                            'film_studio': Film_Studio,
                            'approx_budget': approx_budget,
                            'synopsis': synopsis,
                            'news_and_guides': rotten_data['news'],
                            'more_like_this': rotten_data['more_like_this'],
                            "revenue": rotten_data['revenue'],
                            "producer": rotten_data['producer'],
                            "photos": rotten_data['photos'],
                        }

                        app_data, created = AppData.objects.update_or_create(name=name, release_year=release,
                                                                             defaults=data)
                        if not created:
                            print('Already in DB')

                        data.update({
                            'language': language,
                            'country': country,
                        })

                        end_time = time.perf_counter()  # End time measurement
                        elapsed_time = end_time - start_time
                        print(f"Execution time: {elapsed_time:.2f} seconds")

                        return JsonResponse(data, safe=False, content_type="application/json")

            except Exception as e:
                print(f"An error occurred: {e}")
                return JsonResponse({"error": f"An error occurred: {e}"}, status=500)

    @staticmethod
    def extract_text(response, selector):
        element = response.html.find(selector, first=True)
        return element.text.strip() if element else None

    @staticmethod
    def extract_text_strip(response, selector, strip_text):
        element = response.html.find(selector, first=True)
        return element.text.replace(strip_text, '').strip() if element else None

    @staticmethod
    def extract_attr(response, selector, attr, index):
        elements = response.html.find(selector)
        return elements[index].attrs[attr].strip() if elements and len(elements) > index else None

    @staticmethod
    def extract_language_country(response, selectors, key_text, model):
        for selector in selectors:
            element = response.html.find(selector, first=True)
            if element:
                text = element.text.replace(key_text, '').strip()
                instance, _ = model.objects.get_or_create(name=text)
                return text, instance
        return None, None


import time
import concurrent.futures
from requests_html import HTMLSession
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view


def fetch_actor_info(actor_element, sess):
    actor_info = {}

    # Extracting actor name
    actor_name_element = actor_element.find('.ipc-title-link-wrapper > h3', first=True)
    actor_info['name'] = actor_name_element.text.strip() if actor_name_element else None

    # Extracting actor page URL
    get_link = actor_element.find('.ipc-title-link-wrapper', first=True)
    if not get_link:
        return None

    actor_url = f"https://www.imdb.com{get_link.attrs['href']}"

    # Extracting thumbnail URL
    thumbnail_element = actor_element.find('div.ipc-metadata-list-summary-item__c img', first=True)
    actor_info['thumbnail'] = thumbnail_element.attrs['src'].strip() if thumbnail_element else None

    # Check if any required value is None, if so, skip adding this actor's info
    if None in actor_info.values():
        return None

    try:
        with sess.get(actor_url) as actor_response:
            actor_response.raise_for_status()

            # Selector for total movie count
            movie_count_selector = '#actor-previous-projects > div.ipc-accordion__item__header.ipc-accordion__item__header--sticky > label > span.ipc-accordion__item__title > ul > li.ipc-inline-list__item.credits-total'
            total_movies_element = actor_response.html.find(movie_count_selector, first=True)
            actor_info['total_movies'] = total_movies_element.text.strip() if total_movies_element else 'Not available'

    except Exception as e:
        # Log the detailed error message
        print(f"Error fetching data for {actor_info['name']}: {str(e)}")
        return None

    return actor_info


class Popular_actors(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        start_time = time.perf_counter()
        try:
            with HTMLSession() as sess:
                url = "https://www.imdb.com/chart/starmeter/"
                response = sess.get(url)

                # Check if the request was successful
                response.raise_for_status()

                # CSS selector to find actor elements
                actor_selector = 'div.ipc-page-content-container section div.ipc-page-grid div ul li'

                popular_actors_data = []
                actor_elements = response.html.find(actor_selector)
                with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
                    future_to_actor = {executor.submit(fetch_actor_info, actor_element, sess): actor_element for actor_element in actor_elements}
                    for future in concurrent.futures.as_completed(future_to_actor):
                        actor_element = future_to_actor[future]
                        try:
                            actor_info = future.result()
                            if actor_info:
                                popular_actors_data.append(actor_info)
                        except Exception as e:
                            print(f"Error processing actor: {str(e)}")

                Popular_Actors_Data = {
                    "Popular_Actors": popular_actors_data,
                }

                end_time = time.perf_counter()
                print(f"Execution time: {end_time - start_time} seconds")

                return Response(Popular_Actors_Data)
        except Exception as e:
            # Log the detailed error message
            print(f"Error: {str(e)}")
            error_message = {"error": "An error occurred while fetching data from IMDb."}
            end_time = time.perf_counter()
            print(f"Execution time: {end_time - start_time} seconds")
            return Response(error_message, status=500)


class ActorAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # Fetch the page containing the profile image URL
            profile_url = "https://www.imdb.com/find/?q=Rebecca%20Ferguson(I)&ref_=nv_sr_sm"
            profile_sess = HTMLSession()
            profile_response = profile_sess.get(profile_url)

            # Extract the profile image URL
            profile_image_src = profile_response.html.find(
                'meta[property="og:image"]', first=True).attrs.get('content', "Not available")

            # Now, proceed with the original scraping logic
            url = "https://www.imdb.com/name/nm0272581/?ref_=fn_al_nm_1"
            sess = HTMLSession()
            response = sess.get(url)

            actor = {}

            actor['profile_image'] = profile_image_src

            bio_element = response.html.find(
                '#__next main div section div section div.sc-491663c0-4.yjUiO div.sc-491663c0-6.lnlBxO div.sc-491663c0-10.rbXFE section div',
                first=True)
            if bio_element:
                actor['bio'] = bio_element.text.strip()
            else:
                actor['bio'] = "Not available"

            birth_date_element = response.html.find(
                '#__next > main > div > section.ipc-page-background.ipc-page-background--base.sc-304f99f6-0.fSJiHR > section > div:nth-child(5) > section > section > div.sc-491663c0-4.yjUiO > div.sc-491663c0-6.lnlBxO > div.sc-491663c0-11.cvvyMK > section > aside > div > span:nth-child(2)',
                first=True)
            if birth_date_element:
                birth_date = birth_date_element.text.strip()
                actor['birth_date'] = birth_date
                # Calculate age from birth date
                try:
                    birth_date_obj = datetime.strptime(birth_date, '%B %d, %Y')
                    today = datetime.today()
                    age = today.year - birth_date_obj.year - (
                            (today.month, today.day) < (birth_date_obj.month, birth_date_obj.day))
                    actor['age'] = age
                except ValueError:
                    actor['age'] = "Not available"
            else:
                actor['birth_date'] = "Not available"
                actor['age'] = "Not available"

            upcoming_movie_element = response.html.find(
                '#accordion-item-actress-upcoming-projects > div',
                first=True)
            if upcoming_movie_element:
                actor['upcoming_movies'] = upcoming_movie_element.text.strip()
            else:
                actor['upcoming_movie'] = "Not available"

            career_element = response.html.find(
                '#actress-previous-projects div.ipc-accordion__item__header.ipc-accordion__item__header--sticky label span.ipc-accordion__item__title ul li.ipc-inline-list__item.credits-total',
                first=True)
            if career_element:
                actor['career'] = {'movies_count': career_element.text.strip()}
            else:
                actor['career'] = {'movies_count': "Not available"}

            response_data = {
                "status": "success",
                "data": {
                    "actor": actor
                }
            }

            return Response(response_data)

        except Exception as e:
            return Response({"status": "error", "message": str(e)})


import concurrent.futures
import threading
import time
from requests_html import HTMLSession
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import datetime
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import threading
from requests_html import HTMLSession
from rest_framework.views import APIView
from rest_framework.response import Response


class ActorsDetail(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        start_time = time.perf_counter()
        try:
            name = request.query_params.get('name')
            if not name:
                return Response({"status": "error", "message": "Name parameter is required."}, status=400)

            name = name.replace(' ', '_')
            name = ''.join(e for e in name if e.isalnum() or e == '_')
            rt_base_url = "https://www.rottentomatoes.com/celebrity/"
            rt_url = f"{rt_base_url}{name}"

            sess = HTMLSession()
            rt_response = sess.get(rt_url)

            actor = {}
            series = []
            movies = []

            def scrape_actor_data():
                try:
                    actor_name_element = rt_response.html.find('#celebrity > article > section:nth-child(1) > div > div > h1', first=True)
                    actor['name'] = actor_name_element.text.strip() if actor_name_element else "Not available"

                    profile_image_element = rt_response.html.find('#celebrity > article > section:nth-child(1) > div > a > img', first=True)
                    actor['profile_image'] = profile_image_element.attrs['src'] if profile_image_element else "Not available"

                    bio_element = rt_response.html.find('#celebrity > article > section:nth-child(1) > div > div > div > drawer-more', first=True)
                    actor['bio'] = bio_element.text.strip() if bio_element else "Not available"

                    birth_date_element = rt_response.html.find('#celebrity > article > section:nth-child(1) > div > div > div > p:nth-child(3)', first=True)
                    if birth_date_element:
                        birth_date = birth_date_element.text.strip()
                        actor['birth_date'] = birth_date
                        try:
                            birth_date_obj = datetime.strptime(birth_date, '%B %d, %Y')
                            today = datetime.today()
                            age = today.year - birth_date_obj.year - ((today.month, today.day) < (birth_date_obj.month, birth_date_obj.day))
                            actor['age'] = age
                        except ValueError:
                            actor['age'] = "Not available"
                    else:
                        actor['birth_date'] = "Not available"
                        actor['age'] = "Not available"

                    highest_rated_movie_element = rt_response.html.find('#celebrity > article > section:nth-child(1) > div > div > div > p:nth-child(1)', first=True)
                    actor['highest_rated_movie'] = highest_rated_movie_element.text.strip() if highest_rated_movie_element else "Not available"
                except Exception as e:
                    print(f"Error scraping actor data: {e}")

            def scrape_series_data():
                try:
                    filmography_section = rt_response.html.find('#celebrity > article > section.celebrity-filmography > div > div:nth-child(4) > table', first=True)
                    if filmography_section:
                        series_rows = filmography_section.find('table > tbody > tr')

                        def scrape_serie_data(row):
                            series_item = {}
                            title = row.find('td.celebrity-filmography__title', first=True)
                            series_item['title'] = title.text.strip() if title else "Not available"

                            year = row.find('td.celebrity-filmography__year', first=True)
                            series_item['year'] = year.text.strip().split()[0] if year else "Not available"

                            rating = row.find('td:nth-child(1) > span > span.icon__tomatometer-score', first=True)
                            series_item['rating'] = float(rating.text.strip().replace('%', '')) if rating else "Not available"

                            imdb_rating = row.find('td:nth-child(2) > span > span.icon__tomatometer-score', first=True)
                            series_item['imdb_rating'] = float(imdb_rating.text.strip().replace('%', '')) if imdb_rating else "Not available"

                            movie_url = f"https://www.rottentomatoes.com/tv/{title.text.strip().replace(' ', '_').lower()}"
                            movie_response = sess.get(movie_url)
                            thumbnail_tag = movie_response.html.find('#modules-wrap > div.media-scorecard.no-border > media-scorecard > rt-img', first=True)
                            series_item['thumbnail'] = thumbnail_tag.attrs['src'] if thumbnail_tag else "Not available"
                            return series_item

                        with ThreadPoolExecutor(max_workers=15) as executor:
                            series.extend(list(executor.map(scrape_serie_data, series_rows)))
                except Exception as e:
                    print(f"Error scraping series data: {e}")

            def scrape_netflix_movies_data():
                try:
                    filmography_section_movies = rt_response.html.find('#celebrity > article > section.celebrity-filmography', first=True)
                    if filmography_section_movies:
                        movies_rows = filmography_section_movies.find('table > tbody > tr')

                        def scrape_movie_data(row):
                            movie_item = {}
                            title = row.find('td.celebrity-filmography__title', first=True)
                            movie_item['title'] = title.text.strip() if title else "Not available"

                            year = row.find('td.celebrity-filmography__year', first=True)
                            movie_item['year'] = year.text.strip().split()[0] if year else "Not available"

                            rating = row.find('td:nth-child(1) > span', first=True)
                            movie_item['rating'] = rating.text.strip() if rating else "Not available"

                            imdb_rating = row.find('td:nth-child(2) > span > span.icon__tomatometer-score', first=True)
                            movie_item['imdb_rating'] = float(imdb_rating.text.strip().replace('%', '')) if imdb_rating else "Not available"

                            movie_url = f"https://www.rottentomatoes.com/m/{title.text.strip().replace(' ', '_').lower()}"
                            movie_response = sess.get(movie_url)
                            thumbnail_tag = movie_response.html.find('#topSection > div.thumbnail-scoreboard-wrap > div > tile-dynamic > rt-img', first=True)
                            movie_item['thumbnail'] = thumbnail_tag.attrs['src'] if thumbnail_tag else "Not available"

                            return movie_item

                        with ThreadPoolExecutor(max_workers=15) as executor:
                            movies.extend(list(executor.map(scrape_movie_data, movies_rows)))
                except Exception as e:
                    print(f"Error scraping movies data: {e}")

            threads = [
                threading.Thread(target=scrape_actor_data),
                threading.Thread(target=scrape_series_data),
                threading.Thread(target=scrape_netflix_movies_data)
            ]

            for thread in threads:
                thread.start()

            for thread in threads:
                thread.join()

            actor["series_count"] = len(series) if series else None
            actor["movies_count"] = len(movies) if movies else None
            actor["followers"] = None

            response_data = {
                "status": "success",
                "data": {
                    "actor": actor,
                    "filmography": {
                        "series": series,
                        "movies": movies,
                    }
                }
            }

            end_time = time.perf_counter()
            print(f"Total execution time: {end_time - start_time} seconds")

            return Response(response_data)

        except Exception as e:
            end_time = time.perf_counter()
            print(f"Total execution time: {end_time - start_time} seconds")
            return Response({"status": "error", "message": str(e)})


class get_upcoming_movies(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            sess = HTMLSession()
            url = "https://www.rottentomatoes.com/browse/movies_coming_soon/"
            response = sess.get(url)
            upcoming_movie_selector = '#main-page-content > div.discovery > div.discovery-grids-container > div'
            upcoming_elements = response.html.find(upcoming_movie_selector)

            if upcoming_elements:
                upcoming_content = []
                with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                    future_to_movie = {executor.submit(scrape_netflix_movies_data, element): element for element in
                                       upcoming_elements[0].find('a')}
                    for future in concurrent.futures.as_completed(future_to_movie):
                        element = future_to_movie[future]
                        try:
                            movie_data = future.result()
                            upcoming_content.append(movie_data)
                        except Exception as e:
                            error_message = {"error": str(e)}
                            return JsonResponse(error_message, status=500)
            else:
                upcoming_content = None

            Content_Data = {
                "Upcoming_Movies": upcoming_content,
            }

            return JsonResponse(Content_Data)
        except Exception as e:
            error_message = {"error": str(e)}
            return JsonResponse(error_message, status=500)


class Top_Netflix_Movie(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            sess = HTMLSession()
            url = "https://www.rottentomatoes.com/browse/movies_at_home/affiliates:netflix"
            response = sess.get(url)
            Netflix_selector = '#main-page-content > div.discovery > div.discovery-grids-container > div'
            Netflix_elements = response.html.find(Netflix_selector)

            if Netflix_elements:
                Netflix_movies = []
                with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                    future_to_movie = {executor.submit(scrape_moviess_data, actor_element): actor_element for actor_element
                                       in
                                       Netflix_elements[0].find('a')[:5]}  # Limiting to top 5 movies
                    for future in concurrent.futures.as_completed(future_to_movie):
                        actor_element = future_to_movie[future]
                        try:
                            movie_data = future.result()
                            Netflix_movies.append(movie_data)
                        except Exception as e:
                            error_message = {"error": str(e)}
                            return JsonResponse(error_message, status=500)
            else:
                Netflix_movies = None

            Movies_Data = {
                "Top_5_Netflix_Movies": Netflix_movies,
            }

            return JsonResponse(Movies_Data)
        except Exception as e:
            error_message = {"error": str(e)}
            return JsonResponse(error_message, status=500)


class New_Movies(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            sess = HTMLSession()
            url = "https://www.rottentomatoes.com/browse/movies_at_home/sort:newest"
            response = sess.get(url)
            New_Movies_selector = '#main-page-content > div.discovery > div.discovery-grids-container > div'
            New_Movies_elements = response.html.find(New_Movies_selector)

            if New_Movies_elements:
                New_Movies_data = []
                with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
                    future_to_movie = {executor.submit(scrape_moviess_data, actor_element): actor_element for actor_element
                                       in
                                       New_Movies_elements[0].find('a')}
                    for future in concurrent.futures.as_completed(future_to_movie):
                        actor_element = future_to_movie[future]
                        try:
                            movie_data = future.result()
                            New_Movies_data.append(movie_data)
                        except Exception as e:
                            error_message = {"error": str(e)}
                            return JsonResponse(error_message, status=500)
            else:
                New_Movies_data = None

            Movies_Data = {
                "New_Movies": New_Movies_data,
            }

            return JsonResponse(Movies_Data)
        except Exception as e:
            error_message = {"error": str(e)}
            return JsonResponse(error_message, status=500)


class new_seasons(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            sess = HTMLSession()
            url = "https://www.rottentomatoes.com/browse/tv_series_browse/sort:newest"
            response = sess.get(url)
            new_seasons_selector = '#main-page-content > div.discovery > div.discovery-grids-container > div'
            new_seasons_elements = response.html.find(new_seasons_selector)

            if new_seasons_elements:
                new_seasons_data = []
                with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                    future_to_season = {executor.submit(scrape_season_data_netflix_hulu_amazon, element): element for element in
                                        new_seasons_elements[0].find('a')}
                    for future in concurrent.futures.as_completed(future_to_season):
                        element = future_to_season[future]
                        try:
                            season_data = future.result()
                            new_seasons_data.append(season_data)
                        except Exception as e:
                            error_message = {"error": str(e)}
                            return JsonResponse(error_message, status=500)
            else:
                new_seasons_data = None

            seasons_data = {
                "new_seasons": new_seasons_data,
            }

            return JsonResponse(seasons_data)
        except Exception as e:
            error_message = {"error": str(e)}
            return JsonResponse(error_message, status=500)


class Top_Netflix_Season(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            sess = HTMLSession()
            url = "https://www.rottentomatoes.com/browse/tv_series_browse/affiliates:netflix~sort:popular"
            response = sess.get(url)
            Netflix_selector = '#main-page-content > div.discovery > div.discovery-grids-container > div'
            Netflix_elements = response.html.find(Netflix_selector)

            if Netflix_elements:
                Netflix_seasons = []
                with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                    future_to_season = {executor.submit(scrape_season_data_netflix_hulu_amazon, season_element): season_element for
                                        season_element in Netflix_elements[0].find('a')[:5]}  # Limiting to top 5 seasons
                    for future in concurrent.futures.as_completed(future_to_season):
                        season_element = future_to_season[future]
                        try:
                            season_data = future.result()
                            Netflix_seasons.append(season_data)
                        except Exception as e:
                            error_message = {"error": str(e)}
                            return JsonResponse(error_message, status=500)
            else:
                Netflix_seasons = None

            Seasons_Data = {
                "Top_5_Netflix_Seasons": Netflix_seasons,
            }

            return JsonResponse(Seasons_Data)
        except Exception as e:
            error_message = {"error": str(e)}
            return JsonResponse(error_message, status=500)


class get_upcoming_season(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            sess = HTMLSession()
            url = "https://www.rottentomatoes.com/browse/movies_coming_soon/"
            response = sess.get(url)
            upcoming_movie_selector = '#main-page-content > div.discovery > div.discovery-grids-container > div'
            upcoming_elements = response.html.find(upcoming_movie_selector)

            if upcoming_elements:
                upcoming_content = []
                with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                    future_to_movie = {executor.submit(scrape_Movie_data, element): element for element in
                                       upcoming_elements[0].find('a')}
                    for future in concurrent.futures.as_completed(future_to_movie):
                        element = future_to_movie[future]
                        try:
                            movie_data = future.result()
                            upcoming_content.append(movie_data)
                        except Exception as e:
                            error_message = {"error": str(e)}
                            return JsonResponse(error_message, status=500)
            else:
                upcoming_content = None

            Content_Data = {
                "Upcoming_Seasons": upcoming_content,
            }

            return JsonResponse(Content_Data)
        except Exception as e:
            error_message = {"error": str(e)}
            return JsonResponse(error_message, status=500)


class Netflix_upcoming_movies(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            sess = HTMLSession()
            url = "https://www.rottentomatoes.com/browse/movies_at_home/affiliates:netflix"
            response = sess.get(url)
            upcoming_movie_selector = '#main-page-content > div.discovery > div.discovery-grids-container > div'
            upcoming_elements = response.html.find(upcoming_movie_selector)

            if upcoming_elements:
                upcoming_content = []
                with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
                    future_to_movie = {executor.submit(scrape_netflix_movies_data, element): element for element in
                                       upcoming_elements[0].find('a')}
                    for future in concurrent.futures.as_completed(future_to_movie):
                        element = future_to_movie[future]
                        try:
                            movie_data = future.result()
                            upcoming_content.append(movie_data)
                        except Exception as e:
                            error_message = {"error": str(e)}
                            return JsonResponse(error_message, status=500)
            else:
                upcoming_content = None

            Content_Data = {
                "Netflix_Movies": upcoming_content,
            }

            return JsonResponse(Content_Data)
        except Exception as e:
            error_message = {"error": str(e)}
            return JsonResponse(error_message, status=500)


class Netflix_New_Movies(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            sess = HTMLSession()
            url = "https://www.rottentomatoes.com/browse/movies_at_home/affiliates:netflix~sort:newest"
            response = sess.get(url)
            New_Movies_selector = '#main-page-content > div.discovery > div.discovery-grids-container > div'
            New_Movies_elements = response.html.find(New_Movies_selector)

            if New_Movies_elements:
                New_Movies_data = []
                with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
                    future_to_movie = {executor.submit(scrape_moviess_data, actor_element): actor_element for actor_element
                                       in
                                       New_Movies_elements[0].find('a')}
                    for future in concurrent.futures.as_completed(future_to_movie):
                        actor_element = future_to_movie[future]
                        try:
                            movie_data = future.result()
                            New_Movies_data.append(movie_data)
                        except Exception as e:
                            error_message = {"error": str(e)}
                            return JsonResponse(error_message, status=500)
            else:
                New_Movies_data = None

            Movies_Data = {
                "New_Movies": New_Movies_data,
            }

            return JsonResponse(Movies_Data)
        except Exception as e:
            error_message = {"error": str(e)}
            return JsonResponse(error_message, status=500)


class Netflix_upcoming_season(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            sess = HTMLSession()
            url = "https://www.rottentomatoes.com/browse/movies_coming_soon/"
            response = sess.get(url)
            upcoming_movie_selector = '#main-page-content > div.discovery > div.discovery-grids-container > div'
            upcoming_elements = response.html.find(upcoming_movie_selector)

            if upcoming_elements:
                upcoming_content = []
                with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                    future_to_movie = {executor.submit(scrape_Movie_data, element): element for element in
                                       upcoming_elements[0].find('a')}
                    for future in concurrent.futures.as_completed(future_to_movie):
                        element = future_to_movie[future]
                        try:
                            movie_data = future.result()
                            upcoming_content.append(movie_data)
                        except Exception as e:
                            error_message = {"error": str(e)}
                            return JsonResponse(error_message, status=500)
            else:
                upcoming_content = None

            Content_Data = {
                "Netflix_Seasons": upcoming_content,
            }

            return JsonResponse(Content_Data)
        except Exception as e:
            error_message = {"error": str(e)}
            return JsonResponse(error_message, status=500)


class Netflix_new_seasons(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            sess = HTMLSession()
            url = "https://www.rottentomatoes.com/browse/tv_series_browse/affiliates:netflix~sort:newest"
            response = sess.get(url)
            new_seasons_selector = '#main-page-content > div.discovery > div.discovery-grids-container > div'
            new_seasons_elements = response.html.find(new_seasons_selector)

            if new_seasons_elements:
                new_seasons_data = []
                with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
                    future_to_season = {executor.submit(scrape_season_data_netflix_hulu_amazon, element): element for element in
                                        new_seasons_elements[0].find('a')}
                    for future in concurrent.futures.as_completed(future_to_season):
                        element = future_to_season[future]
                        try:
                            season_data = future.result()
                            new_seasons_data.append(season_data)
                        except Exception as e:
                            error_message = {"error": str(e)}
                            return JsonResponse(error_message, status=500)
            else:
                new_seasons_data = None

            seasons_data = {
                "new_seasons": new_seasons_data,
            }

            return JsonResponse(seasons_data)
        except Exception as e:
            error_message = {"error": str(e)}
            return JsonResponse(error_message, status=500)


class Hulu_Movies_data(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            sess = HTMLSession()
            url = "https://www.rottentomatoes.com/browse/movies_at_home/affiliates:hulu"
            response = sess.get(url)
            upcoming_movie_selector = '#main-page-content > div.discovery > div.discovery-grids-container > div'
            upcoming_elements = response.html.find(upcoming_movie_selector)

            if upcoming_elements:
                upcoming_content = []
                with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                    future_to_movie = {executor.submit(scrape_netflix_movies_data, element): element for element in
                                       upcoming_elements[0].find('a')}
                    for future in concurrent.futures.as_completed(future_to_movie):
                        element = future_to_movie[future]
                        try:
                            movie_data = future.result()
                            upcoming_content.append(movie_data)
                        except Exception as e:
                            error_message = {"error": str(e)}
                            return JsonResponse(error_message, status=500)
            else:
                upcoming_content = None

            Content_Data = {
                "Hulu_Movies": upcoming_content,
            }

            return JsonResponse(Content_Data)
        except Exception as e:
            error_message = {"error": str(e)}
            return JsonResponse(error_message, status=500)


class Hulu_New_Movies(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            sess = HTMLSession()
            url = "https://www.rottentomatoes.com/browse/movies_at_home/affiliates:hulu~sort:newest"
            response = sess.get(url)
            New_Movies_selector = '#main-page-content > div.discovery > div.discovery-grids-container > div'
            New_Movies_elements = response.html.find(New_Movies_selector)

            if New_Movies_elements:
                New_Movies_data = []
                with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
                    future_to_movie = {executor.submit(scrape_moviess_data, actor_element): actor_element for actor_element
                                       in
                                       New_Movies_elements[0].find('a')}
                    for future in concurrent.futures.as_completed(future_to_movie):
                        actor_element = future_to_movie[future]
                        try:
                            movie_data = future.result()
                            New_Movies_data.append(movie_data)
                        except Exception as e:
                            error_message = {"error": str(e)}
                            return JsonResponse(error_message, status=500)
            else:
                New_Movies_data = None

            Movies_Data = {
                "New_Movies": New_Movies_data,
            }

            return JsonResponse(Movies_Data)
        except Exception as e:
            error_message = {"error": str(e)}
            return JsonResponse(error_message, status=500)


class Hulu_season_data(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            sess = HTMLSession()
            url = "https://www.rottentomatoes.com/browse/tv_series_browse/affiliates:hulu"
            response = sess.get(url)
            upcoming_movie_selector = '#main-page-content > div.discovery > div.discovery-grids-container > div'
            upcoming_elements = response.html.find(upcoming_movie_selector)

            if upcoming_elements:
                upcoming_content = []
                with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                    future_to_movie = {executor.submit(scrape_Movie_data, element): element for element in
                                       upcoming_elements[0].find('a')}
                    for future in concurrent.futures.as_completed(future_to_movie):
                        element = future_to_movie[future]
                        try:
                            movie_data = future.result()
                            upcoming_content.append(movie_data)
                        except Exception as e:
                            error_message = {"error": str(e)}
                            return JsonResponse(error_message, status=500)
            else:
                upcoming_content = None

            Content_Data = {
                "Hulu_Seasons": upcoming_content,
            }

            return JsonResponse(Content_Data)
        except Exception as e:
            error_message = {"error": str(e)}
            return JsonResponse(error_message, status=500)


class Hulu_new_seasons(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request):
        try:
            sess = HTMLSession()
            url = "https://www.rottentomatoes.com/browse/tv_series_browse/affiliates:hulu~sort:newest"
            response = sess.get(url)
            new_seasons_selector = '#main-page-content > div.discovery > div.discovery-grids-container > div'
            new_seasons_elements = response.html.find(new_seasons_selector)

            if new_seasons_elements:
                new_seasons_data = []
                with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
                    future_to_season = {executor.submit(scrape_season_data_netflix_hulu_amazon, element): element for element in
                                        new_seasons_elements[0].find('a')}
                    for future in concurrent.futures.as_completed(future_to_season):
                        element = future_to_season[future]
                        try:
                            season_data = future.result()
                            new_seasons_data.append(season_data)
                        except Exception as e:
                            error_message = {"error": str(e)}
                            return JsonResponse(error_message, status=500)
            else:
                new_seasons_data = None

            seasons_data = {
                "new_seasons": new_seasons_data,
            }

            return JsonResponse(seasons_data)
        except Exception as e:
            error_message = {"error": str(e)}
            return JsonResponse(error_message, status=500)


class AmazonPrime_Movies_data(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            sess = HTMLSession()
            url = "https://www.rottentomatoes.com/browse/tv_series_browse/affiliates:amazon_prime"
            response = sess.get(url)
            upcoming_movie_selector = '#main-page-content > div.discovery > div.discovery-grids-container > div'
            upcoming_elements = response.html.find(upcoming_movie_selector)

            if upcoming_elements:
                upcoming_content = []
                with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                    future_to_movie = {executor.submit(scrape_netflix_movies_data, element): element for element in
                                       upcoming_elements[0].find('a')}
                    for future in concurrent.futures.as_completed(future_to_movie):
                        element = future_to_movie[future]
                        try:
                            movie_data = future.result()
                            upcoming_content.append(movie_data)
                        except Exception as e:
                            error_message = {"error": str(e)}
                            return JsonResponse(error_message, status=500)
            else:
                upcoming_content = None

            Content_Data = {
                "AmazonPrime_Movies": upcoming_content,
            }

            return JsonResponse(Content_Data)
        except Exception as e:
            error_message = {"error": str(e)}
            return JsonResponse(error_message, status=500)


class AmazonPrime_New_Movies(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request):
        try:
            sess = HTMLSession()
            url = "https://www.rottentomatoes.com/browse/tv_series_browse/affiliates:amazon_prime~sort:newest"
            response = sess.get(url)
            New_Movies_selector = '#main-page-content > div.discovery > div.discovery-grids-container > div'
            New_Movies_elements = response.html.find(New_Movies_selector)

            if New_Movies_elements:
                New_Movies_data = []
                with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
                    future_to_movie = {executor.submit(scrape_moviess_data, actor_element): actor_element for actor_element
                                       in
                                       New_Movies_elements[0].find('a')}
                    for future in concurrent.futures.as_completed(future_to_movie):
                        actor_element = future_to_movie[future]
                        try:
                            movie_data = future.result()
                            New_Movies_data.append(movie_data)
                        except Exception as e:
                            error_message = {"error": str(e)}
                            return JsonResponse(error_message, status=500)
            else:
                New_Movies_data = None

            Movies_Data = {
                "New_Movies": New_Movies_data,
            }

            return JsonResponse(Movies_Data)
        except Exception as e:
            error_message = {"error": str(e)}
            return JsonResponse(error_message, status=500)


class AmazonPrime_season_data(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            sess = HTMLSession()
            url = "https://www.rottentomatoes.com/browse/tv_series_browse/affiliates:amazon_prime"
            response = sess.get(url)
            upcoming_movie_selector = '#main-page-content > div.discovery > div.discovery-grids-container > div'
            upcoming_elements = response.html.find(upcoming_movie_selector)

            if upcoming_elements:
                upcoming_content = []
                with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                    future_to_movie = {executor.submit(scrape_Movie_data, element): element for element in
                                       upcoming_elements[0].find('a')}
                    for future in concurrent.futures.as_completed(future_to_movie):
                        element = future_to_movie[future]
                        try:
                            movie_data = future.result()
                            upcoming_content.append(movie_data)
                        except Exception as e:
                            error_message = {"error": str(e)}
                            return JsonResponse(error_message, status=500)
            else:
                upcoming_content = None

            Content_Data = {
                "Hulu_Seasons": upcoming_content,
            }

            return JsonResponse(Content_Data)
        except Exception as e:
            error_message = {"error": str(e)}
            return JsonResponse(error_message, status=500)


class AmazonPrime_new_seasons(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            sess = HTMLSession()
            url = "https://www.rottentomatoes.com/browse/tv_series_browse/affiliates:amazon_prime~sort:newest"
            response = sess.get(url)
            new_seasons_selector = '#main-page-content > div.discovery > div.discovery-grids-container > div'
            new_seasons_elements = response.html.find(new_seasons_selector)

            if new_seasons_elements:
                new_seasons_data = []
                with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
                    future_to_season = {executor.submit(scrape_season_data_netflix_hulu_amazon, element): element for element in
                                        new_seasons_elements[0].find('a')}
                    for future in concurrent.futures.as_completed(future_to_season):
                        element = future_to_season[future]
                        try:
                            season_data = future.result()
                            new_seasons_data.append(season_data)
                        except Exception as e:
                            error_message = {"error": str(e)}
                            return JsonResponse(error_message, status=500)
            else:
                new_seasons_data = None

            seasons_data = {
                "new_seasons": new_seasons_data,
            }

            return JsonResponse(seasons_data)
        except Exception as e:
            error_message = {"error": str(e)}
            return JsonResponse(error_message, status=500)
















# class scrape_netflix_movies_dataView(APIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#
#     def get(self, request):
#         try:
#             movie_name = request.GET.get('movie_name')
#             movie_name = movie_name.replace(' ', '_')
#             movie_name = ''.join(e for e in movie_name if e.isalnum() or e == '_')
#             url = f'https://www.rottentomatoes.com/m/{movie_name}'
#
#             session = HTMLSession()
#             r = session.get(url)
#
#             scoreboard_element = r.html.find('#scoreboard > h1', first=True)
#             scoreboard = scoreboard_element.text if scoreboard_element else None
#
#             released_date_element = r.html.find('#info > li:nth-child(7)', first=True)
#             released_date = released_date_element.text if released_date_element else None
#
#             duration_element = r.html.find('#info > li:nth-child(8) > p > span', first=True)
#             duration = duration_element.text if duration_element else None
#
#             original_language_element = r.html.find('#info > li:nth-child(3) > p > span', first=True)
#             original_language = original_language_element.text if original_language_element else None
#
#             movie_type = 'Movie'
#
#             info_element = r.html.find('#movie-info > div > div > drawer-more > p', first=True)
#             info = info_element.text if info_element else None
#
#             audience_score = '#scoreboard'
#             audience_score = r.html.find(audience_score)
#             if audience_score:
#                 score = audience_score[0].attrs['audiencescore']
#                 score = score + '%' if score else ''
#             else:
#                 score = None
#
#             rotten_rating = '#scoreboard'
#             rotten_rating = r.html.find(rotten_rating)
#             if rotten_rating:
#                 rating = rotten_rating[0].attrs['tomatometerscore']
#                 rating = rating + '%' if rating else ''
#             else:
#                 rating = None
#
#             imdb_rating = None
#
#             status = None
#
#             year_element = r.html.find('#info > li:nth-child(7) > p > span > time', first=True)
#             year = year_element.text if year_element else None
#
#             genre_element = r.html.find('#info > li:nth-child(2) > p > span', first=True)
#             genre = genre_element.text if genre_element else None
#
#             view = None
#
#             result = {
#                 "name": scoreboard,
#                 "released_date": released_date,
#                 "duration": duration,
#                 "original_language": original_language,
#                 "type": movie_type,
#                 "info": info,
#                 "Status": status,
#                 "Audience_Score": score,
#                 "R.Tomatoes": rating,
#                 "IMDb": imdb_rating,
#                 "Year": year,
#                 "Genre": genre,
#                 "Views": view
#             }
#
#             return JsonResponse(result)
#
#         except Exception as e:
#             return JsonResponse({"error": str(e)}, status=500)


# def scrape_movie_data(element):
#     try:
#         sess = HTMLSession()
#         movie_data = {}
#         movie_data['title'] = element.text.strip()
#         movie_url = f"https://www.rottentomatoes.com{element.attrs['href']}"
#         movie_response = sess.get(movie_url)
#
#         # Extracting release date
#         release_date = movie_response.html.find('#info > li:nth-child(5) > p > span > time', first=True)
#         movie_data['release_date'] = release_date.text if release_date else ""
#
#         # Extracting rating
#         rotten_rating = '#scoreboard'
#         rotten_rating = movie_response.html.find(rotten_rating)
#         if rotten_rating:
#             rating = rotten_rating[0].attrs['tomatometerscore']
#             movie_data['rating'] = rating + '%' if rating else ''
#         else:
#             rating = None
#
#         # IMDb rating
#         movie_data['imdb_rating'] = None
#
#         # Extracting thumbnail
#         thumbnail = movie_response.html.find(
#             '#topSection > div.thumbnail-scoreboard-wrap > div > tile-dynamic > rt-img', first=True)
#         movie_data['thumbnail'] = thumbnail.attrs['src'] if thumbnail else ""
#
#         movie_data['Views'] = 5.8
#
#         return movie_data
#     except Exception as e:
#         return {"error": str(e)}
## class Netflix_Movie(APIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#
#     def get(self, request):
#         try:
#             # movie_name = request.GET['movie_name']
#             sess = HTMLSession()
#             url = "https://www.rottentomatoes.com/browse/movies_at_home/affiliates:netflix"
#             response = sess.get(url)
#             Netflix_selector = '#main-page-content > div.discovery > div.discovery-grids-container > div'
#             Netflix_elements = response.html.find(Netflix_selector)
#
#             if Netflix_elements:
#                 Netflix_movies = []
#                 for actor_element in Netflix_elements[0].find('a'):
#                     actor_name = actor_element.text
#                     # actor_url = actor_element.attrs['href']
#                     if actor_name:
#                         Netflix_movies.append(actor_name.strip())
#             else:
#                 Netflix_movies = None
#
#             Movies_Data = {
#                 "Top_Netflix_movies": Netflix_movies,
#             }
#
#             return JsonResponse(Movies_Data)
#         except Exception as e:
#
#             error_message = {"error": str(e)}
#             return JsonResponse(error_message, status=500)


# class Upcoming_Movies(APIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#
#     def get(self, request):
#         try:
#             sess = HTMLSession()
#             url = "https://www.rottentomatoes.com/browse/movies_at_home/affiliates:netflix"
#             response = sess.get(url)
#             upcoming_movie_selector = '#main-page-content > div.discovery > div.discovery-grids-container'
#             upcoming_elements = response.html.find(upcoming_movie_selector)
#
#             if upcoming_elements:
#                 upcoming_content = []
#                 for element in upcoming_elements[0].find('a'):
#                     content_name = element.text
#                     # content_url = element.attrs['href']
#                     if content_name:
#                         upcoming_content.append(content_name.strip())
#             else:
#                 upcoming_content = None
#
#             Content_Data = {
#                 "Upcoming_Movies/Series": upcoming_content,
#             }
#
#             return JsonResponse(Content_Data)
#         except Exception as e:
#             error_message = {"error": str(e)}
#             return JsonResponse(error_message, status=500)
#
#
# class Season_tv_shows(APIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#
#     def get(self, request):
#         try:
#             sess = HTMLSession()
#             url = "https://www.imdb.com/chart/tvmeter/"
#             response = sess.get(url)
#             season_tv_shows_selector = '#__next > main > div > div.ipc-page-content-container.ipc-page-content-container--center > section > div > div.ipc-page-grid.ipc-page-grid--bias-left > div'
#             season_tv_shows_elements = response.html.find(season_tv_shows_selector)
#
#             if season_tv_shows_elements:
#                 season_tv_shows = []
#                 for show_element in season_tv_shows_elements[0].find('a'):
#                     show_name = show_element.text
#                     # show_url = show_element.attrs['href']
#                     if show_name:
#                         season_tv_shows.append(show_name.strip())
#             else:
#                 season_tv_shows = None
#
#             Season_Tv_Shows_Data = {
#                 "Season_Tv_Shows": season_tv_shows,
#             }
#
#             return JsonResponse(Season_Tv_Shows_Data)
#         except Exception as e:
#             error_message = {"error": str(e)}
#             return JsonResponse(error_message, status=500)
#
#
# class All_Movies(APIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#
#     def get(self, request):
#         try:
#             sess = HTMLSession()
#             url = "https://www.rottentomatoes.com/browse/movies_in_theaters/"
#             response = sess.get(url)
#             theaters_selector = '#main-page-content > div.discovery > div.discovery-grids-container > div'
#             theaters_elements = response.html.find(theaters_selector)
#
#             if theaters_elements:
#                 theaters_movies = []
#                 for movie_element in theaters_elements[0].find('a'):
#                     movie_name = movie_element.text
#                     # movie_url = movie_element.attrs['href']
#                     if movie_name:
#                         theaters_movies.append(movie_name.strip())
#             else:
#                 theaters_movies = None
#
#             Movies_Data = {
#                 "Movies": theaters_movies,
#             }
#
#             return JsonResponse(Movies_Data)
#         except Exception as e:
#             error_message = {"error": str(e)}
#             return JsonResponse(error_message, status=500)
#
# class imdb(APIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#
#     def get(self, request):
#         try:
#             movie_name = request.GET.get('movie_name')
#             if not movie_name:
#                 return JsonResponse({"error": "Movie name not provided"})
#
#             # Search for the movie on Rotten Tomatoes
#             sess = HTMLSession()
#             rotten_search_url = f"https://www.rottentomatoes.com/search?search={movie_name}"
#             rotten_search_response = sess.get(rotten_search_url)
#
#
#             # Extracting movie title from search results
#             title_element = rotten_search_response.html.find('.movieTitle a')
#             if not title_element:
#                 return JsonResponse({"error": "Movie not found on Rotten Tomatoes"})
#
#             movie_title = title_element[0].text.strip()
#
#             # Scrape reviews from IMDb based on the movie title
#             imdb_reviews_url = f"https://www.imdb.com/title/{movie_title}/reviews"
#             imdb_reviews_response = sess.get(imdb_reviews_url)
#
#             # Extracting reviews
#             reviews_selector = '#main > section > div.lister > div.lister-list > div'
#             reviews_elements = imdb_reviews_response.html.find(reviews_selector)
#             reviews_data = []
#
#             for review_element in reviews_elements:
#                 # Extracting username
#                 username_element = review_element.find('span.display-name-link > a')
#                 username = username_element[0].text.strip() if username_element else None
#
#                 # Extracting post date
#                 postdate_element = review_element.find('span.review-date')
#                 postdate = postdate_element[0].text.strip() if postdate_element else None
#
#                 # Extracting comment text
#                 comment_element = review_element.find('div.content > div.text.show-more__control')
#                 comment = comment_element[0].text.strip() if comment_element else None
#
#                 reviews_data.append({
#                     "userName": username,
#                     "postdate": postdate,
#                     "comment": comment
#                 })
#
#             return JsonResponse(reviews_data, safe=False)
#
#         except Exception as e:
#             return JsonResponse({"error": f"An error occurred: {e}"})
#
