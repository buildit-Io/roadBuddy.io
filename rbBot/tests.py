from requests.api import patch
from rbBot.views import rbHookView
from rbBot.models import Location, PlanningSession, Route, User
from django.test import TestCase, RequestFactory
from unittest import mock
from unittest.mock import call
import json

# Create your tests here.

# test database
# test creating a new user
# test separation of multiple users
# test logic of user behaviour
# test multiple users behaviour doesnt clash

# APICALLS INTEGRATION TEST



# MODELS TEST

class ModelUserTest(TestCase):
    # Tests default fields
    def test_default(self):
        default_user = User()
        default_user.user_id=1
        default_user.save()
        got = User.objects.first()
        want = User()
        want = User()
        want.user_id = 1
        want.first_name = "null"
        want.last_name = "null"
        want.username = "null"
        want.is_started = True
        want.is_planning = False
        want.planning_route = 0
        want.routes_created = 0
        self.assertEqual(got, want)
        
    # Tests that multiple users can be stored
    def test_saving_and_retrieving_Users(self):
        # create 2 test users
        first_user = User()
        first_user.user_id = 2
        first_user.first_name = "first"
        first_user.last_name = "last"
        first_user.username = "firstusername"
        first_user.is_started = False
        first_user.is_planning = False
        first_user.planning_route = 1
        first_user.routes_created = 1
        first_user.save()
        second_user = User()
        second_user.user_id = 1
        second_user.first_name = "second"
        second_user.last_name = "last"
        second_user.username = "secondusername"
        second_user.is_started = True
        second_user.is_planning = True
        second_user.planning_route = 2
        second_user.routes_created = 2
        second_user.save()
        
        got = User.objects.all()
        
        # users should be sorted by id
        self.assertEqual(got[0], second_user)
        self.assertEqual(got[1], first_user)
        
class ModelPlanningSessionTest(TestCase):
    def test_saving_and_retrieving_sessions(self):
        default_user = User()
        default_user.user_id=1
        default_user.save()
        first = PlanningSession()
        first.chat_id = 2
        first.message_id = 2
        first.instance = 2
        first.message = 2
        first.user = default_user
        first.save()
        second = PlanningSession()
        second.chat_id = 1
        second.message_id = 3
        second.instance = 3
        second.message = 3
        second.user = default_user
        second.save()
        
        got = PlanningSession.objects.all()
        # test sorted by chat_id
        self.assertEqual(got[0], second)
        self.assertEqual(got[1], first)

class ModelRouteTest(TestCase):
    def test_saving_and_retrieving_routes(self):
        # Given
        default_user = User()
        default_user.user_id=1
        default_user.save()
        
        default_session = PlanningSession()
        default_session.chat_id = 2
        default_session.message_id = 2
        default_session.instance = 2
        default_session.message = 2
        default_session.user = default_user
        default_session.save()
        
        # When
        first_route = Route()
        first_route.route_id = 2
        first_route.user = default_user
        first_route.destinations = "{first, second}"
        first_route.current_session = default_session
        first_route.logged = False
        first_route.save()
        second_route = Route()
        second_route.route_id = 1
        second_route.user = default_user
        second_route.destinations = "{second, third}"
        second_route.current_session = None
        second_route.logged = True
        second_route.save()
        
        # Then
        # should ignore routeid order, follow save order
        got = Route.objects.all()
        self.assertEqual(got[0], first_route)
        self.assertEqual(got[1], second_route)
        
        
    def test_delete_planning_session(self):
        # Given
        default_user = User()
        default_user.user_id=1
        default_user.save()
        
        default_session = PlanningSession()
        default_session.chat_id = 2
        default_session.message_id = 2
        default_session.instance = 2
        default_session.message = 2
        default_session.user = default_user
        default_session.save()
        
        # When
        first_route = Route()
        first_route.route_id = 2
        first_route.user = default_user
        first_route.destinations = "{first, second}"
        first_route.current_session = default_session
        first_route.logged = False
        first_route.save()
        default_session.delete()
        
        # Then
        # session field should be set to null when corresponding session is deleted
        self.assertEquals(Route.objects.first().current_session, None)
        
    #TODO: add tests for when user is deleted
        
class ModelLocationTest(TestCase):
    def test_location_save_and_retrieve(self):
        # Given
        default_user = User()
        default_user.user_id=1
        default_user.save()
        
        default_session = PlanningSession()
        default_session.chat_id = 2
        default_session.message_id = 2
        default_session.instance = 2
        default_session.message = 2
        default_session.user = default_user
        default_session.save()
        
        first_route = Route()
        first_route.route_id = 2
        first_route.user = default_user
        first_route.destinations = "{first, second}"
        first_route.current_session = default_session
        first_route.logged = False
        first_route.save()
        second_route = Route()
        second_route.route_id = 1
        second_route.user = default_user
        second_route.destinations = "{second, third}"
        second_route.current_session = None
        second_route.logged = True
        second_route.save()
        
        # When
        first_loc = Location()
        first_loc.postal_code = 152532
        first_loc.long_address = "first location's long address"
        first_loc.longtitude = 123.456789123456789
        first_loc.latitude = 12.456789123456789
        first_loc.save()
        
        first_loc.routes.add(first_route)
        
        second_loc = Location()
        second_loc.postal_code = 152532
        second_loc.long_address = "second location's long address"
        second_loc.longtitude = 123.456789123456789
        second_loc.latitude = 12.456789123456789
        second_loc.save()
        
        # second_loc.route.set(second_route)
        
        # Then
        savedLoc = Location.objects.all()
        self.assertEquals(savedLoc[0], first_loc)
        self.assertEquals(savedLoc[1], second_loc)
    
# This class groups tests on post requests with callback_query data field


class CallbackQueryTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        # create request body containing data from request
        # 1) contains: 'callback_query' field
        
        # 2) contains 'message'
        #   a) contains text
    
    # test post request where user is not recorded in database
    @mock.patch('rbBot.botbrain.reply.requests') # mock telegram posts
    @mock.patch('rbBot.botbrain.reply.TOKEN', "mockToken") # mocks credentials for telegram
    def test_invalid_user(self, teleMock):
        # NOTE: Would have preferred to mock os.getenv instead of token directly, but
        #       unittest sucks I actually spent 3 weeks trying to do this more rigorously
        
        # Given
        instance = 54235
        chat_id = 53425
        body = {
            "callback_query": {
                "from": {
                    "id": 0 # sender, irrelevant
                },
                "id": instance,    # instance
                "message": {
                    "message_id": 0,    # message_id, irrelevant
                    "chat": {
                        "id": chat_id,    # target 
                    }
                },
                
            }
        }
        
        # When
        request = self.factory.post('/rbBot/bot-hook/', data=json.dumps(body),
                                    content_type='application/json')        
        rbHookView.as_view()(request)
        wantedCalls = [call('https://api.telegram.org/botmockToken/answerCallbackQuery', data={'callback_query_id': instance, 'text': 'This message has expired and is no longer valid.', 'show_alert': True, 'url': '', 'cache_time': 0}), 
                       call('https://api.telegram.org/botmockToken/sendMessage', data={'chat_id': chat_id, 'text': 'Please input a valid command', 'parse_mode': 'Markdown'})]
        
        # Then
        self.assertEqual(wantedCalls, teleMock.post.call_args_list)
        
        
        
    def tearDown(self) -> None:
        pass
        
        
        
        

# class logicTest(TestCase):
#     def setUp(self):
#         # TODO: create user(s) to test with
    
    
#     def test_single_user_can_activate(self):
#         fake_user = 327761768
#         fake_message_id = 1007
#         logic.activate(fake_message_id,fake_user)


# TEST HELPERS
# def setup_view(view, request, *args, **kwargs):
#     """
#     Mimic ``as_view()``, but returns view instance.
#     Use this function to get view instances on which you can run unit tests,
#     by testing specific methods.
#     """

#     view.request = request
#     view.args = args
#     view.kwargs = kwargs
#     return view