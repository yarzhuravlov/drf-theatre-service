from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from theatre.models import Play, Actor, Genre, Performance, TheatreHall, Zone, ZonePrice


class PlayViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.actor = Actor.objects.create(first_name="John", last_name="Doe")
        self.genre = Genre.objects.create(name="Drama")
        self.play = Play.objects.create(title="Hamlet", description="A tragedy")
        self.play.actors.add(self.actor)
        self.play.genres.add(self.genre)

    def test_list_plays(self):
        url = reverse("v1:theatre:play-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Hamlet")

    def test_retrieve_play(self):
        url = reverse("v1:theatre:play-detail", args=[self.play.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Hamlet")
        self.assertIn("future_performances", response.data)

    def test_retrieve_nonexistent_play(self):
        url = reverse("v1:theatre:play-list", args=[999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class PerformanceViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.theatre_hall = TheatreHall.objects.create(name="Main Hall")
        self.zone = Zone.objects.create(
            name="VIP", theatre_hall=self.theatre_hall, rows=10, seats_in_row=10
        )
        self.play = Play.objects.create(title="Hamlet", description="A tragedy")
        self.performance = Performance.objects.create(
            play=self.play, theatre_hall=self.theatre_hall, show_time="2025-05-20T19:00:00Z"
        )
        ZonePrice.objects.create(
            zone=self.zone, performance=self.performance, ticket_price=100
        )

    def test_list_performances(self):
        url = reverse("v1:theatre:performance-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["play"]["title"], "Hamlet")

    def test_retrieve_performance(self):
        url = reverse("v1:theatre:performance-detail", args=[self.performance.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["play"]["title"], "Hamlet")
        self.assertIn("zone_prices", response.data)

    def test_retrieve_nonexistent_performance(self):
        url = reverse("v1:theatre:performance-detail", args=[999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ActorViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.actor = Actor.objects.create(first_name="John", last_name="Doe")

    def test_list_actors(self):
        url = reverse("v1:theatre:actor-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["first_name"], "John")

    def test_search_actors(self):
        url = reverse("v1:theatre:actor-list") + "?search=John"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["first_name"], "John")

    def test_search_no_results(self):
        url = reverse("v1:theatre:actor-list") + "?search=Jane"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)


class GenreViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.genre = Genre.objects.create(name="Drama")

    def test_list_genres(self):
        url = reverse("v1:theatre:genre-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Drama")

    def test_search_genres(self):
        url = reverse("v1:theatre:genre-list") + "?search=Drama"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Drama")

    def test_search_no_results(self):
        url = reverse("v1:theatre:genre-list") + "?search=Comedy"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)