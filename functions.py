from rest_framework.views import APIView
from requests_html import HTMLSession, Element
from datetime import datetime
from requests_html import HTMLSession
from django.http import JsonResponse


def scrape_season_data_netflix_hulu_amazon(element):
    try:
        sess = HTMLSession()
        season_data = {}
        season_data['title'] = element.text.strip()
        season_url = f"https://www.rottentomatoes.com{element.attrs['href']}"
        season_response = sess.get(season_url)

        # Extracting release date
        release_date = season_response.html.find(
            '#modules-wrap > div:nth-child(11) > section > div.content-wrap > dl > div:nth-child(6)', first=True)
        season_data['release_date'] = release_date.text.strip() if release_date else ""

        rating = season_response.html.find(
            '#modules-wrap > div.media-scorecard.no-border > media-scorecard > rt-text:nth-child(3)', first=True)
        season_data['rating'] = rating.text.strip() if rating else ""

        # IMDb rating
        imdb_url = "https://www.imdb.com/search/title/?title=" + element.text.strip().replace(" ", " ")
        index = imdb_url.find(" Streaming")
        desired_url = imdb_url[:index]
        imdb_response = sess.get(desired_url)
        imdb_rating_selector = "#__next > main > div.ipc-page-content-container.ipc-page-content-container--center.sc-4ce8cf2c-0.efkzGq > div.ipc-page-content-container.ipc-page-content-container--center > section > section > div > section > section > div:nth-child(2) > div > section > div.ipc-page-grid.ipc-page-grid--bias-left.ipc-page-grid__item.ipc-page-grid__item--span-2 > div.ipc-page-grid__item.ipc-page-grid__item--span-2 > ul > li:nth-child(1) > div > div > div > div.sc-ab6fa25a-2.gOsifL > div.sc-b0691f29-0.jbYPfh > span > div > span"
        imdb_rating = imdb_response.html.find(imdb_rating_selector, first=True)
        if imdb_rating:
            imdb_rating_text = imdb_rating.text.strip()
            imdb_rating_numeric = imdb_rating_text.split()[0]
            try:
                season_data['imdb_rating'] = float(imdb_rating_numeric)
            except ValueError:
                season_data['imdb_rating'] = "Not available"
        else:
            season_data['imdb_rating'] = "Not available"

            # Extracting thumbnail
        thumbnail = season_response.html.find(
            '#modules-wrap > div.media-scorecard.no-border > media-scorecard > rt-img', first=True)
        season_data['thumbnail'] = thumbnail.attrs['src'] if thumbnail else ""

        return season_data
    except Exception as e:
        return {"error": str(e)}


def scrape_season_data_netflix_hulu_amazon(element):
    try:
        sess = HTMLSession()
        season_data = {}
        season_data['title'] = element.text.strip()
        season_url = f"https://www.rottentomatoes.com{element.attrs['href']}"
        season_response = sess.get(season_url)

        # Extracting release date
        release_date = season_response.html.find(
            '#modules-wrap > div:nth-child(11) > section > div.content-wrap > dl > div:nth-child(6)', first=True)
        season_data['release_date'] = release_date.text.strip() if release_date else ""

        rating = season_response.html.find(
            '#modules-wrap > div.media-scorecard.no-border > media-scorecard > rt-text:nth-child(3)', first=True)
        season_data['rating'] = rating.text.strip() if rating else ""

        # IMDb rating
        imdb_url = "https://www.imdb.com/search/title/?title=" + element.text.strip().replace(" ", " ")
        index = imdb_url.find(" Streaming")
        desired_url = imdb_url[:index]
        imdb_response = sess.get(desired_url)
        imdb_rating_selector = "#__next > main > div.ipc-page-content-container.ipc-page-content-container--center.sc-4ce8cf2c-0.efkzGq > div.ipc-page-content-container.ipc-page-content-container--center > section > section > div > section > section > div:nth-child(2) > div > section > div.ipc-page-grid.ipc-page-grid--bias-left.ipc-page-grid__item.ipc-page-grid__item--span-2 > div.ipc-page-grid__item.ipc-page-grid__item--span-2 > ul > li:nth-child(1) > div > div > div > div.sc-ab6fa25a-2.gOsifL > div.sc-b0691f29-0.jbYPfh > span > div > span"
        imdb_rating = imdb_response.html.find(imdb_rating_selector, first=True)
        if imdb_rating:
            imdb_rating_text = imdb_rating.text.strip()
            imdb_rating_numeric = imdb_rating_text.split()[0]
            try:
                season_data['imdb_rating'] = float(imdb_rating_numeric)
            except ValueError:
                season_data['imdb_rating'] = "Not available"
        else:
            season_data['imdb_rating'] = "Not available"

            # Extracting thumbnail
        thumbnail = season_response.html.find(
            '#modules-wrap > div.media-scorecard.no-border > media-scorecard > rt-img', first=True)
        season_data['thumbnail'] = thumbnail.attrs['src'] if thumbnail else ""

        return season_data
    except Exception as e:
        return {"error": str(e)}

def scrape_season_data_netflix_hulu_amazon(element):
    try:
        sess = HTMLSession()
        season_data = {}
        season_data['title'] = element.text.strip()
        season_url = f"https://www.rottentomatoes.com{element.attrs['href']}"
        season_response = sess.get(season_url)

        # Extracting release date
        release_date = season_response.html.find(
            '#modules-wrap > div:nth-child(11) > section > div.content-wrap > dl > div:nth-child(6)', first=True)
        season_data['release_date'] = release_date.text.strip() if release_date else ""

        rating = season_response.html.find(
            '#modules-wrap > div.media-scorecard.no-border > media-scorecard > rt-text:nth-child(3)', first=True)
        season_data['rating'] = rating.text.strip() if rating else ""

        # IMDb rating
        imdb_url = "https://www.imdb.com/search/title/?title=" + element.text.strip().replace(" ", " ")
        index = imdb_url.find(" Streaming")
        desired_url = imdb_url[:index]
        imdb_response = sess.get(desired_url)
        imdb_rating_selector = "#__next > main > div.ipc-page-content-container.ipc-page-content-container--center.sc-4ce8cf2c-0.efkzGq > div.ipc-page-content-container.ipc-page-content-container--center > section > section > div > section > section > div:nth-child(2) > div > section > div.ipc-page-grid.ipc-page-grid--bias-left.ipc-page-grid__item.ipc-page-grid__item--span-2 > div.ipc-page-grid__item.ipc-page-grid__item--span-2 > ul > li:nth-child(1) > div > div > div > div.sc-ab6fa25a-2.gOsifL > div.sc-b0691f29-0.jbYPfh > span > div > span"
        imdb_rating = imdb_response.html.find(imdb_rating_selector, first=True)
        if imdb_rating:
            imdb_rating_text = imdb_rating.text.strip()
            imdb_rating_numeric = imdb_rating_text.split()[0]
            try:
                season_data['imdb_rating'] = float(imdb_rating_numeric)
            except ValueError:
                season_data['imdb_rating'] = "Not available"
        else:
            season_data['imdb_rating'] = "Not available"

            # Extracting thumbnail
        thumbnail = season_response.html.find(
            '#modules-wrap > div.media-scorecard.no-border > media-scorecard > rt-img', first=True)
        season_data['thumbnail'] = thumbnail.attrs['src'] if thumbnail else ""

        return season_data
    except Exception as e:
        return {"error": str(e)}


def scrape_season_data_netflix_hulu_amazon(element):
    try:
        season_data = {}
        season_data['title'] = element.text.strip()
        season_url = f"https://www.rottentomatoes.com{element.attrs['href']}"

        with HTMLSession() as sess:
            season_response = sess.get(season_url, verify=False)
            season_response.raise_for_status()  # Ensure the request was successful

            # Extracting release date
            release_date = season_response.html.find(
                '#modules-wrap > div:nth-child(11) > section > div.content-wrap > dl > div:nth-child(6)', first=True)
            season_data['release_date'] = release_date.text.strip() if release_date else "Not available"

            # Extracting rating
            rating = season_response.html.find(
                '#modules-wrap > div.media-scorecard.no-border > media-scorecard > rt-text:nth-child(3)', first=True)
            season_data['rating'] = rating.text.strip() if rating else "Not available"

            # IMDb rating
            imdb_search_url = "https://www.imdb.com/search/title/?title=" + element.text.strip().replace(" ", "+")
            imdb_response = sess.get(imdb_search_url, verify=False)
            imdb_response.raise_for_status()  # Ensure the request was successful

            imdb_rating_selector = "#__next main div.ipc-page-content-container.ipc-page-content-container--center.sc-4ce8cf2c-0.efkzGq div.ipc-page-content-container.ipc-page-content-container--center section section div section section div:nth-child(2) div section div.ipc-page-grid.ipc-page-grid--bias-left.ipc-page-grid__item.ipc-page-grid__item--span-2 div.ipc-page-grid__item.ipc-page-grid__item--span-2 ul li:nth-child(1) div div div div.sc-ab6fa25a-2.gOsifL div.sc-b0691f29-0.jbYPfh span div span"
            imdb_rating = imdb_response.html.find(imdb_rating_selector, first=True)
            if imdb_rating:
                imdb_rating_text = imdb_rating.text.strip()
                imdb_rating_numeric = imdb_rating_text.split()[0]
                try:
                    season_data['imdb_rating'] = float(imdb_rating_numeric)
                except ValueError:
                    season_data['imdb_rating'] = "Not available"
            else:
                season_data['imdb_rating'] = "Not available"

            # Extracting thumbnail
            thumbnail = season_response.html.find(
                '#modules-wrap > div.media-scorecard.no-border > media-scorecard > rt-img', first=True)
            season_data['thumbnail'] = thumbnail.attrs['src'] if thumbnail else "Not available"

        return season_data
    except Exception as e:
        return {"error": str(e)}


def scrape_season_data_netflix_hulu_amazon(element):
    try:
        sess = HTMLSession()
        season_data = {}
        season_data['title'] = element.text.strip()
        season_url = f"https://www.rottentomatoes.com{element.attrs['href']}"
        season_response = sess.get(season_url)

        # Extracting release date
        release_date = season_response.html.find(
            '#modules-wrap > div:nth-child(11) > section > div.content-wrap > dl > div:nth-child(6)', first=True)
        season_data['release_date'] = release_date.text.strip() if release_date else ""

        rating = season_response.html.find(
            '#modules-wrap > div.media-scorecard.no-border > media-scorecard > rt-text:nth-child(3)', first=True)
        season_data['rating'] = rating.text.strip() if rating else ""

        # IMDb rating
        imdb_url = "https://www.imdb.com/search/title/?title=" + element.text.strip().replace(" ", " ")
        index = imdb_url.find(" Streaming")
        desired_url = imdb_url[:index]
        imdb_response = sess.get(desired_url)
        imdb_rating_selector = "#__next > main > div.ipc-page-content-container.ipc-page-content-container--center.sc-4ce8cf2c-0.efkzGq > div.ipc-page-content-container.ipc-page-content-container--center > section > section > div > section > section > div:nth-child(2) > div > section > div.ipc-page-grid.ipc-page-grid--bias-left.ipc-page-grid__item.ipc-page-grid__item--span-2 > div.ipc-page-grid__item.ipc-page-grid__item--span-2 > ul > li:nth-child(1) > div > div > div > div.sc-ab6fa25a-2.gOsifL > div.sc-b0691f29-0.jbYPfh > span > div > span"
        imdb_rating = imdb_response.html.find(imdb_rating_selector, first=True)
        if imdb_rating:
            imdb_rating_text = imdb_rating.text.strip()
            imdb_rating_numeric = imdb_rating_text.split()[0]
            try:
                season_data['imdb_rating'] = float(imdb_rating_numeric)
            except ValueError:
                season_data['imdb_rating'] = "Not available"
        else:
            season_data['imdb_rating'] = "Not available"

            # Extracting thumbnail
        thumbnail = season_response.html.find(
            '#modules-wrap > div.media-scorecard.no-border > media-scorecard > rt-img', first=True)
        season_data['thumbnail'] = thumbnail.attrs['src'] if thumbnail else ""

        return season_data
    except Exception as e:
        return {"error": str(e)}


def scrape_season_data_netflix_hulu_amazon(element):
    try:
        sess = HTMLSession()
        season_data = {}

        if not isinstance(element, Element):
            raise ValueError("Invalid element type. Expected Element object.")

        season_data['title'] = element.text.strip()

        season_url = f"https://www.rottentomatoes.com{element.attrs['href']}"
        season_response = sess.get(season_url)

        # Ensure successful response
        if season_response.status_code != 200:
            raise ValueError(
                f"Failed to fetch data for season: {season_data['title']}. Status code: {season_response.status_code}")

        # Extracting release date
        release_date = season_response.html.find(
            '#modules-wrap > div:nth-child(13) > section > div.content-wrap > dl > div:nth-child(8)', first=True)
        season_data['release_date'] = release_date.text.strip() if release_date else ""

        # Extracting rating
        rating = season_response.html.find(
            '#modules-wrap > div.media-scorecard.no-border > media-scorecard > rt-text:nth-child(3)', first=True)
        season_data['rating'] = rating.text.strip() if rating else ""

        # IMDb rating
        imdb_rating_selector = "#modules-wrap > div.media-scorecard.no-border > media-scorecard > rt-text:nth-child(3) > span > a"
        imdb_rating = season_response.html.find(imdb_rating_selector, first=True)
        season_data['imdb_rating'] = imdb_rating.text.strip() if imdb_rating else ""

        # Extracting thumbnail
        thumbnail = season_response.html.find(
            '#modules-wrap > div.media-scorecard.no-border > media-scorecard > rt-img', first=True)
        season_data['thumbnail'] = thumbnail.attrs['src'] if thumbnail else ""

        return season_data
    except Exception as e:
        return {"error": str(e)}

def scrape_season_data_netflix_hulu_amazon(element):
    try:
        sess = HTMLSession()
        season_data = {}
        season_data['title'] = element.text.strip()
        season_url = f"https://www.rottentomatoes.com{element.attrs['href']}"
        season_response = sess.get(season_url)

        # Extracting release date
        release_date = season_response.html.find(
            '#modules-wrap > div:nth-child(11) > section > div.content-wrap > dl > div:nth-child(6)', first=True)
        season_data['release_date'] = release_date.text.strip() if release_date else ""

        rating = season_response.html.find(
            '#modules-wrap > div.media-scorecard.no-border > media-scorecard > rt-text:nth-child(3)', first=True)
        season_data['rating'] = rating.text.strip() if rating else ""

        # IMDb rating
        imdb_url = "https://www.imdb.com/search/title/?title=" + element.text.strip().replace(" ", " ")
        index = imdb_url.find(" Streaming")
        desired_url = imdb_url[:index]
        imdb_response = sess.get(desired_url)
        imdb_rating_selector = "#__next > main > div.ipc-page-content-container.ipc-page-content-container--center.sc-4ce8cf2c-0.efkzGq > div.ipc-page-content-container.ipc-page-content-container--center > section > section > div > section > section > div:nth-child(2) > div > section > div.ipc-page-grid.ipc-page-grid--bias-left.ipc-page-grid__item.ipc-page-grid__item--span-2 > div.ipc-page-grid__item.ipc-page-grid__item--span-2 > ul > li:nth-child(1) > div > div > div > div.sc-ab6fa25a-2.gOsifL > div.sc-b0691f29-0.jbYPfh > span > div > span"
        imdb_rating = imdb_response.html.find(imdb_rating_selector, first=True)
        if imdb_rating:
            imdb_rating_text = imdb_rating.text.strip()
            imdb_rating_numeric = imdb_rating_text.split()[0]
            try:
                season_data['imdb_rating'] = float(imdb_rating_numeric)
            except ValueError:
                season_data['imdb_rating'] = "Not available"
        else:
            season_data['imdb_rating'] = "Not available"

            # Extracting thumbnail
        thumbnail = season_response.html.find(
            '#modules-wrap > div.media-scorecard.no-border > media-scorecard > rt-img', first=True)
        season_data['thumbnail'] = thumbnail.attrs['src'] if thumbnail else ""

        return season_data
    except Exception as e:
        return {"error": str(e)}


def scrape_netflix_movies_data(element):
    try:
        sess = HTMLSession()
        movie_data = {}

        if not isinstance(element, Element):
            raise ValueError("Invalid element type. Expected Element object.")

        movie_data['title'] = element.text.strip()

        movie_url = f"https://www.rottentomatoes.com{element.attrs['href']}"
        movie_response = sess.get(movie_url)

        # Ensure successful response
        if movie_response.status_code != 200:
            raise ValueError(
                f"Failed to fetch data for movie: {movie_data['title']}. Status code: {movie_response.status_code}")

        # Extracting release date
        release_date = movie_response.html.find('#info > li:nth-child(5) > p > span > time', first=True)
        movie_data['release_date'] = release_date.text if release_date else ""

        # Extracting rating
        rotten_rating = '#scoreboard'
        rotten_rating = movie_response.html.find(rotten_rating)
        if rotten_rating:
            rating = rotten_rating[0].attrs['tomatometerscore']
            movie_data['rating'] = rating + '%' if rating else ''
        else:
            rating = None

        # IMDb rating
        imdb_url = "https://www.imdb.com/search/title/?title=" + element.text.strip().replace(" ", "+")
        imdb_response = sess.get(imdb_url)
        imdb_rating_selector = "#__next > main > div > section.ipc-page-background.ipc-page-background--base.sc-304f99f6-0.fSJiHR > section > div:nth-child(5) > section > section > div.sc-4e4cc5f9-3.dDRspk > div.sc-3a4309f8-0.bjXIAP.sc-b7c53eda-1.iIQkEw > div > div:nth-child(1) > a > span > div > div.sc-bde20123-0.dLwiNw > div.sc-bde20123-2.cdQqzc > span.sc-bde20123-1.cMEQkK"
        imdb_rating = imdb_response.html.find(imdb_rating_selector, first=True)
        if imdb_rating:
            imdb_rating_text = imdb_rating.text.strip()
            imdb_rating_text = imdb_rating_text.replace('%', '')
            movie_data['imdb_rating'] = float(imdb_rating_text)
        else:
            movie_data['imdb_rating'] = "Not available"

        # Extracting thumbnail
        thumbnail = movie_response.html.find(
            '#modules-wrap > div.media-scorecard.no-border > media-scorecard > rt-img', first=True)
        movie_data['thumbnail'] = thumbnail.attrs['src'] if thumbnail else ""

        return movie_data
    except Exception as e:
        return {"error": str(e)}

def scrape_moviess_data(element):
    try:
        sess = HTMLSession()
        movie_data = {}
        movie_data['title'] = element.text.strip()
        movie_url = f"https://www.rottentomatoes.com{element.attrs['href']}"
        movie_response = sess.get(movie_url)

        # Extracting release date
        release_date = movie_response.html.find('#info > li:nth-child(5) > p > span > time', first=True)
        movie_data['release_date'] = release_date.text.strip() if release_date else ""

        # Extracting rating
        rotten_rating = movie_response.html.find('#scoreboard')
        if rotten_rating:
            rating = rotten_rating[0].attrs.get('tomatometerscore')
            movie_data['rating'] = rating + '%' if rating else ''
        else:
            movie_data['rating'] = ""

        # IMDb rating
        imdb_url = "https://www.imdb.com/find?q=" + element.text.strip().replace(" ", "+") + "&ref_=nv_sr_sm"
        imdb_response = sess.get(imdb_url)
        imdb_link = imdb_response.html.find('.result_text a', first=True)
        if imdb_link:
            imdb_movie_url = "https://www.imdb.com" + imdb_link.attrs['href']
            imdb_movie_response = sess.get(imdb_movie_url)
            imdb_rating = imdb_movie_response.html.find('.ratingValue span[itemprop="ratingValue"]', first=True)
            if imdb_rating:
                movie_data['imdb_rating'] = float(imdb_rating.text.strip())
            else:
                movie_data['imdb_rating'] = "Not available"
        else:
            movie_data['imdb_rating'] = "Not available"

        # Extracting thumbnail
        thumbnail = movie_response.html.find('#modules-wrap > div.media-scorecard.no-border > media-scorecard > rt-img',
                                             first=True)
        movie_data['thumbnail'] = thumbnail.attrs['src'] if thumbnail else ""

        return movie_data
    except Exception as e:
        return {"error": str(e)}

def scrape_Movie_data(element):
    try:
        sess = HTMLSession()
        movie_data = {}
        movie_data['title'] = element.text.strip()
        movie_url = f"https://www.rottentomatoes.com{element.attrs['href']}"
        movie_response = sess.get(movie_url)

        # Extracting release date
        release_date = movie_response.html.find('#info > li:nth-child(5) > p > span > time', first=True)
        movie_data['release_date'] = release_date.text if release_date else ""

        # Extracting rating
        rotten_rating = '#scoreboard'
        rotten_rating = movie_response.html.find(rotten_rating)
        if rotten_rating:
            rating = rotten_rating[0].attrs['tomatometerscore']
            movie_data['rating'] = rating + '%' if rating else ''
        else:
            rating = None

        # IMDb rating
        movie_data['imdb_rating'] = None

        # Extracting thumbnail
        thumbnail = movie_response.html.find(
            '#modules-wrap > div.media-scorecard.no-border > media-scorecard > rt-img', first=True)
        movie_data['thumbnail'] = thumbnail.attrs['src'] if thumbnail else ""

        movie_data['Views'] = 5.8

        return movie_data
    except Exception as e:
        return {"error": str(e)}

def scrape_netflix_movies_data(element):
    try:
        sess = HTMLSession()
        movie_data = {}

        if not isinstance(element, Element):
            raise ValueError("Invalid element type. Expected Element object.")

        movie_data['title'] = element.text.strip()

        movie_url = f"https://www.rottentomatoes.com{element.attrs['href']}"
        movie_response = sess.get(movie_url)

        # Ensure successful response
        if movie_response.status_code != 200:
            raise ValueError(
                f"Failed to fetch data for movie: {movie_data['title']}. Status code: {movie_response.status_code}")

        # Extracting release date
        release_date = movie_response.html.find('#info > li:nth-child(5) > p > span > time', first=True)
        movie_data['release_date'] = release_date.text if release_date else ""

        # Extracting rating
        rotten_rating = '#scoreboard'
        rotten_rating = movie_response.html.find(rotten_rating)
        if rotten_rating:
            rating = rotten_rating[0].attrs['tomatometerscore']
            movie_data['rating'] = rating + '%' if rating else ''
        else:
            rating = None

        # IMDb rating
        imdb_url = "https://www.imdb.com/search/title/?title=" + element.text.strip().replace(" ", "+")
        imdb_response = sess.get(imdb_url)
        imdb_rating_selector = "#__next > main > div > section.ipc-page-background.ipc-page-background--base.sc-304f99f6-0.fSJiHR > section > div:nth-child(5) > section > section > div.sc-4e4cc5f9-3.dDRspk > div.sc-3a4309f8-0.bjXIAP.sc-b7c53eda-1.iIQkEw > div > div:nth-child(1) > a > span > div > div.sc-bde20123-0.dLwiNw > div.sc-bde20123-2.cdQqzc > span.sc-bde20123-1.cMEQkK"
        imdb_rating = imdb_response.html.find(imdb_rating_selector, first=True)
        if imdb_rating:
            imdb_rating_text = imdb_rating.text.strip()
            imdb_rating_text = imdb_rating_text.replace('%', '')
            movie_data['imdb_rating'] = float(imdb_rating_text)
        else:
            movie_data['imdb_rating'] = "Not available"

        # Extracting thumbnail
        thumbnail = movie_response.html.find(
            '#modules-wrap > div.media-scorecard.no-border > media-scorecard > rt-img', first=True)
        movie_data['thumbnail'] = thumbnail.attrs['src'] if thumbnail else ""

        return movie_data
    except Exception as e:
        return {"error": str(e)}

def scrape_Movie_data(element):
    try:
        sess = HTMLSession()
        movie_data = {}
        movie_data['title'] = element.text.strip()
        movie_url = f"https://www.rottentomatoes.com{element.attrs['href']}"
        movie_response = sess.get(movie_url)

        # Extracting release date
        release_date = movie_response.html.find('#info > li:nth-child(5) > p > span > time', first=True)
        movie_data['release_date'] = release_date.text if release_date else ""

        # Extracting rating
        rotten_rating = '#scoreboard'
        rotten_rating = movie_response.html.find(rotten_rating)
        if rotten_rating:
            rating = rotten_rating[0].attrs['tomatometerscore']
            movie_data['rating'] = rating + '%' if rating else ''
        else:
            rating = None

        # IMDb rating
        movie_data['imdb_rating'] = None

        # Extracting thumbnail
        thumbnail = movie_response.html.find(
            '#modules-wrap > div.media-scorecard.no-border > media-scorecard > rt-img', first=True)
        movie_data['thumbnail'] = thumbnail.attrs['src'] if thumbnail else ""

        movie_data['Views'] = 5.8

        return movie_data
    except Exception as e:
        return {"error": str(e)}

def scrape_netflix_movies_data(element):
    try:
        sess = HTMLSession()
        movie_data = {}

        if not isinstance(element, Element):
            raise ValueError("Invalid element type. Expected Element object.")

        movie_data['title'] = element.text.strip()

        movie_url = f"https://www.rottentomatoes.com{element.attrs['href']}"
        movie_response = sess.get(movie_url)

        # Ensure successful response
        if movie_response.status_code != 200:
            raise ValueError(
                f"Failed to fetch data for movie: {movie_data['title']}. Status code: {movie_response.status_code}")

        # Extracting release date
        release_date = movie_response.html.find('#info > li:nth-child(5) > p > span > time', first=True)
        movie_data['release_date'] = release_date.text if release_date else ""

        # Extracting rating
        rotten_rating = '#scoreboard'
        rotten_rating = movie_response.html.find(rotten_rating)
        if rotten_rating:
            rating = rotten_rating[0].attrs['tomatometerscore']
            movie_data['rating'] = rating + '%' if rating else ''
        else:
            rating = None

        # IMDb rating
        imdb_url = "https://www.imdb.com/search/title/?title=" + element.text.strip().replace(" ", "+")
        imdb_response = sess.get(imdb_url)
        imdb_rating_selector = "#__next > main > div > section.ipc-page-background.ipc-page-background--base.sc-304f99f6-0.fSJiHR > section > div:nth-child(5) > section > section > div.sc-4e4cc5f9-3.dDRspk > div.sc-3a4309f8-0.bjXIAP.sc-b7c53eda-1.iIQkEw > div > div:nth-child(1) > a > span > div > div.sc-bde20123-0.dLwiNw > div.sc-bde20123-2.cdQqzc > span.sc-bde20123-1.cMEQkK"
        imdb_rating = imdb_response.html.find(imdb_rating_selector, first=True)
        if imdb_rating:
            imdb_rating_text = imdb_rating.text.strip()
            imdb_rating_text = imdb_rating_text.replace('%', '')
            movie_data['imdb_rating'] = float(imdb_rating_text)
        else:
            movie_data['imdb_rating'] = "Not available"

        # Extracting thumbnail
        thumbnail = movie_response.html.find(
            '#modules-wrap > div.media-scorecard.no-border > media-scorecard > rt-img', first=True)
        movie_data['thumbnail'] = thumbnail.attrs['src'] if thumbnail else ""

        return movie_data
    except Exception as e:
        return {"error": str(e)}


def scrape_moviess_data(element):
    try:
        sess = HTMLSession()
        movie_data = {}
        movie_data['title'] = element.text.strip()
        movie_url = f"https://www.rottentomatoes.com{element.attrs['href']}"
        movie_response = sess.get(movie_url)

        # Extracting release date
        release_date = movie_response.html.find('#info > li:nth-child(5) > p > span > time', first=True)
        movie_data['release_date'] = release_date.text.strip() if release_date else ""

        # Extracting rating
        rotten_rating = movie_response.html.find('#scoreboard')
        if rotten_rating:
            rating = rotten_rating[0].attrs.get('tomatometerscore')
            movie_data['rating'] = rating + '%' if rating else ''
        else:
            movie_data['rating'] = ""

        # IMDb rating
        imdb_url = "https://www.imdb.com/find?q=" + element.text.strip().replace(" ", "+") + "&ref_=nv_sr_sm"
        imdb_response = sess.get(imdb_url)
        imdb_link = imdb_response.html.find('.result_text a', first=True)
        if imdb_link:
            imdb_movie_url = "https://www.imdb.com" + imdb_link.attrs['href']
            imdb_movie_response = sess.get(imdb_movie_url)
            imdb_rating = imdb_movie_response.html.find('.ratingValue span[itemprop="ratingValue"]', first=True)
            if imdb_rating:
                movie_data['imdb_rating'] = float(imdb_rating.text.strip())
            else:
                movie_data['imdb_rating'] = "Not available"
        else:
            movie_data['imdb_rating'] = "Not available"

        # Extracting thumbnail
        thumbnail = movie_response.html.find('#modules-wrap > div.media-scorecard.no-border > media-scorecard > rt-img',
                                             first=True)
        movie_data['thumbnail'] = thumbnail.attrs['src'] if thumbnail else ""

        return movie_data
    except Exception as e:
        return {"error": str(e)}

def scrape_Movie_data(element):
    try:
        sess = HTMLSession()
        movie_data = {}
        movie_data['title'] = element.text.strip()
        movie_url = f"https://www.rottentomatoes.com{element.attrs['href']}"
        movie_response = sess.get(movie_url)

        # Extracting release date
        release_date = movie_response.html.find('#info > li:nth-child(5) > p > span > time', first=True)
        movie_data['release_date'] = release_date.text if release_date else ""

        # Extracting rating
        rotten_rating = '#scoreboard'
        rotten_rating = movie_response.html.find(rotten_rating)
        if rotten_rating:
            rating = rotten_rating[0].attrs['tomatometerscore']
            movie_data['rating'] = rating + '%' if rating else ''
        else:
            rating = None

        # IMDb rating
        movie_data['imdb_rating'] = None

        # Extracting thumbnail
        thumbnail = movie_response.html.find(
            '#modules-wrap > div.media-scorecard.no-border > media-scorecard > rt-img', first=True)
        movie_data['thumbnail'] = thumbnail.attrs['src'] if thumbnail else ""

        movie_data['Views'] = 5.8

        return movie_data
    except Exception as e:
        return {"error": str(e)}

def scrape_netflix_movies_data(element):
    try:
        sess = HTMLSession()
        movie_data = {}

        if not isinstance(element, Element):
            raise ValueError("Invalid element type. Expected Element object.")

        movie_data['title'] = element.text.strip()

        movie_url = f"https://www.rottentomatoes.com{element.attrs['href']}"
        movie_response = sess.get(movie_url)

        # Ensure successful response
        if movie_response.status_code != 200:
            raise ValueError(
                f"Failed to fetch data for movie: {movie_data['title']}. Status code: {movie_response.status_code}")

        # Extracting release date
        release_date = movie_response.html.find('#info > li:nth-child(5) > p > span > time', first=True)
        movie_data['release_date'] = release_date.text if release_date else ""

        # Extracting rating
        rotten_rating = '#scoreboard'
        rotten_rating = movie_response.html.find(rotten_rating)
        if rotten_rating:
            rating = rotten_rating[0].attrs['tomatometerscore']
            movie_data['rating'] = rating + '%' if rating else ''
        else:
            rating = None

        # IMDb rating
        imdb_url = "https://www.imdb.com/search/title/?title=" + element.text.strip().replace(" ", "+")
        imdb_response = sess.get(imdb_url)
        imdb_rating_selector = "#__next > main > div > section.ipc-page-background.ipc-page-background--base.sc-304f99f6-0.fSJiHR > section > div:nth-child(5) > section > section > div.sc-4e4cc5f9-3.dDRspk > div.sc-3a4309f8-0.bjXIAP.sc-b7c53eda-1.iIQkEw > div > div:nth-child(1) > a > span > div > div.sc-bde20123-0.dLwiNw > div.sc-bde20123-2.cdQqzc > span.sc-bde20123-1.cMEQkK"
        imdb_rating = imdb_response.html.find(imdb_rating_selector, first=True)
        if imdb_rating:
            imdb_rating_text = imdb_rating.text.strip()
            imdb_rating_text = imdb_rating_text.replace('%', '')
            movie_data['imdb_rating'] = float(imdb_rating_text)
        else:
            movie_data['imdb_rating'] = "Not available"

        # Extracting thumbnail
        thumbnail = movie_response.html.find(
            '#modules-wrap > div.media-scorecard.no-border > media-scorecard > rt-img', first=True)
        movie_data['thumbnail'] = thumbnail.attrs['src'] if thumbnail else ""

        return movie_data
    except Exception as e:
        return {"error": str(e)}


def scrape_Movie_data(element):
    try:
        sess = HTMLSession()
        movie_data = {}
        movie_data['title'] = element.text.strip()
        movie_url = f"https://www.rottentomatoes.com{element.attrs['href']}"
        movie_response = sess.get(movie_url)

        # Extracting release date
        release_date = movie_response.html.find('#info > li:nth-child(5) > p > span > time', first=True)
        movie_data['release_date'] = release_date.text if release_date else ""

        # Extracting rating
        rotten_rating = '#scoreboard'
        rotten_rating = movie_response.html.find(rotten_rating)
        if rotten_rating:
            rating = rotten_rating[0].attrs['tomatometerscore']
            movie_data['rating'] = rating + '%' if rating else ''
        else:
            rating = None

        # IMDb rating
        movie_data['imdb_rating'] = None

        # Extracting thumbnail
        thumbnail = movie_response.html.find(
            '#modules-wrap > div.media-scorecard.no-border > media-scorecard > rt-img', first=True)
        movie_data['thumbnail'] = thumbnail.attrs['src'] if thumbnail else ""

        movie_data['Views'] = 5.8

        return movie_data
    except Exception as e:
        return {"error": str(e)}

