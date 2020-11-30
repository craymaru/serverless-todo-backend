import pytest

from chalice import BadRequestError

from chalicelib.validates import Validates

from tests.testdata.ddb_items import TESTDATA_DDB_ITEMS
from tests.testdata.non_str_types import TESTDATA_NON_STR_TYPES


class TestValidates:
    pass


class TestValidatesSubject(TestValidates):

    @pytest.mark.parametrize('subject', [item['subject'] for item in TESTDATA_DDB_ITEMS])
    def test_Pass_case_normal(self, subject):
        """subject: 通常 のケース、例外をパスできる"""
        assert Validates.subject(subject) == None

    def test_Raise_BadRequestError_case_None(self):
        """subject: None のケース、例外を発生させることができる"""
        with pytest.raises(BadRequestError):
            Validates.subject(None)

    @pytest.mark.parametrize('bad_type_subject', TESTDATA_NON_STR_TYPES)
    def test_Raise_BadRequestError_case_bad_type(self, bad_type_subject):
        """subject: str以外の型 のケース、例外を発生させることができる"""
        with pytest.raises(BadRequestError):
            Validates.subject(bad_type_subject)

    @pytest.mark.parametrize('boundery_length_subject', [
        '@' * (Validates.SUBJECT_MIN_LEN),
        '@' * (Validates.SUBJECT_MAX_LEN)])
    def test_Pass_case_boundery_length(self, boundery_length_subject):
        """subject: 境界値の限界 のケース、例外をパスできる"""
        assert Validates.subject(boundery_length_subject) == None

    @pytest.mark.parametrize('bad_length_subject', [
        '@' * (Validates.SUBJECT_MIN_LEN - 1),
        '@' * (Validates.SUBJECT_MAX_LEN + 1),
        '@' * (Validates.SUBJECT_MAX_LEN * 10)])
    def test_Raise_BadRequestError_case_boundery_length(self, bad_length_subject):
        """subject: 境界値を超過しているケース、例外を発生させることができる"""
        with pytest.raises(BadRequestError):
            Validates.subject(bad_length_subject)

class TestValidatesDescription(TestValidates):

    @pytest.mark.parametrize('description', [item['description'] for item in TESTDATA_DDB_ITEMS])
    def test_Pass_case_normal(self, description):
        """description: 通常 のケース、例外をパスできる"""
        assert Validates.description(description) == None

    def test_Pass_case_None(self):
        """description: None のケース、例外をパスできる"""
        assert Validates.description(None) == None

    @pytest.mark.parametrize('bad_type_description', TESTDATA_NON_STR_TYPES)
    def test_Raise_BadRequestError_case_bad_type(self, bad_type_description):
        """description: str以外の型 のケース、例外を発生させることができる"""
        with pytest.raises(BadRequestError):
            Validates.description(bad_type_description)

    def test_Pass_case_boundery_legth(self):
        """description: 境界値の限界 のケース、例外をパスできる"""
        assert Validates.description('@'*Validates.DESCRIPTION_MAX_LEN) == None

    @pytest.mark.parametrize('bad_length_description', [
        '@' * (Validates.DESCRIPTION_MAX_LEN + 1),
        '@' * (Validates.DESCRIPTION_MAX_LEN * 10)])
    def test_Raise_BadRequestError_case_boundery_length(self, bad_length_description):
        """description: 境界値を超過しているケース、例外を発生させることができる"""
        with pytest.raises(BadRequestError):
            Validates.description(bad_length_description)

class TestValidatesState(TestValidates):

    @pytest.mark.parametrize('state', [item['state'] for item in TESTDATA_DDB_ITEMS])
    def test_Pass_case_normal(self, state):
        """state: 通常 のケース、例外をパスできる"""
        assert Validates.state(state) == None

    def test_Raise_BadRequestError_case_None(self):
        """state: None のケース、例外を発生させることができる"""
        with pytest.raises(BadRequestError):
            Validates.state(None)

    @pytest.mark.parametrize('bad_type_state', TESTDATA_NON_STR_TYPES)
    def test_Raise_BadRequestError_case_bad_type(self, bad_type_state):
        """state: str以外の型 のケース、例外を発生させることができる"""
        with pytest.raises(BadRequestError):
            Validates.state(bad_type_state)

    @pytest.mark.parametrize('state', Validates.STATE_ENUM)
    def test_Pass_case_state_in_enum(self, state):
        """state: Validates.STATE_ENUMに含まれる場合、例外をパスできる"""
        assert Validates.state(state) == None

    @pytest.mark.parametrize('state', ["unknown_state"] \
        + [state + " " for state in Validates.STATE_ENUM] \
        + [" " + state for state in Validates.STATE_ENUM])
    def test_Raise_BadRequestError_case_not_state_in_enum(self, state):
        """state: Validates.STATE_ENUMに含まれない場合、例外を発生させることができる"""
        with pytest.raises(BadRequestError):
            Validates.state(state)

class TestValidatesUsername(TestValidates):

    # @pytest.mark.parametrize('username', [item['username'] for item in TESTDATA_DDB_ITEMS])
    # def test_Pass_case_normal(self, username):
    #     """username: 通常 のケース、例外をパスできる"""
    #     assert Validates.username(username) == None

    def test_Raise_BadRequestError_case_None(self):
        """username: None のケース、例外を発生させることができる"""
        with pytest.raises(BadRequestError):
            Validates.username(None)

    @pytest.mark.parametrize('bad_type_username', TESTDATA_NON_STR_TYPES)
    def test_Raise_BadRequestError_case_bad_type(self, bad_type_username):
        """username: str以外の型 のケース、例外を発生させることができる"""
        with pytest.raises(BadRequestError):
            Validates.username(bad_type_username)

    @pytest.mark.parametrize('boundery_length_username', [
        '@' * (Validates.USERNAME_MIN_LEN),
        '@' * (Validates.USERNAME_MAX_LEN)])
    def test_Pass_case_boundery_length(self, boundery_length_username):
        """username: 境界値の限界 のケース、例外をパスできる"""
        assert Validates.username(boundery_length_username) == None

    @pytest.mark.parametrize('bad_length_username', [
        '@' * (Validates.USERNAME_MIN_LEN - 1),
        '@' * (Validates.USERNAME_MAX_LEN + 1),
        '@' * (Validates.USERNAME_MAX_LEN * 10)])
    def test_Raise_BadRequestError_case_boundery_length(self, bad_length_username):
        """username: 境界値を超過しているケース、例外を発生させることができる"""
        with pytest.raises(BadRequestError):
            Validates.username(bad_length_username)