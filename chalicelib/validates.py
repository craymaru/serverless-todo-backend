from chalice import BadRequestError

class Validates:

    SUBJECT_MIN_LEN = 1
    SUBJECT_MAX_LEN = 80
    DESCRIPTION_MAX_LEN = 1000
    USERNAME_MIN_LEN = 2
    USERNAME_MAX_LEN = 128
    STATE_ENUM = ["unstarted", "started", "completed"]

    @staticmethod
    def subject(subject):
        if subject is None:
            raise BadRequestError(
                f"Subject is None. (yours: {None})")

        subject_type = type(subject)
        if subject_type is not str:
            raise BadRequestError(
                "Bad subject type. "
                f"REQUIRED: {str} (yours: {subject_type})")

        subject_length = len(subject)
        if not Validates.SUBJECT_MIN_LEN <= subject_length <= Validates.SUBJECT_MAX_LEN:
            raise BadRequestError(
                "Bad subject length. "
                f"REQUIRED: greater than or equal to {Validates.SUBJECT_MIN_LEN}, "
                f"less than or equal to {Validates.SUBJECT_MAX_LEN} "
                f"(yours: {subject_length})")

    @staticmethod
    def description(description):
        description_type = type(description)
        if description_type is not str:
            raise BadRequestError(
                "Bad description type. "
                f"REQUIRED: {str} (yours: {description_type})")

        description_length = len(description)
        if not description_length <= Validates.DESCRIPTION_MAX_LEN:
            raise BadRequestError(
                "Bad subject length. "
                f"REQUIRED: less than or equal to {Validates.DESCRIPTION_MAX_LEN} "
                f"(yours: {description_length})")

    @staticmethod
    def username(username):
        if username is None:
            raise BadRequestError(
                f"Username is None. (yours: {None})")

        username_type = type(username)
        if username_type is not str:
            raise BadRequestError(
                "Bad username type. "
                f"REQUIRED: {str} (yours: {username_type})")

        username_length = len(username)
        if not Validates.USERNAME_MIN_LEN <= username_length <= Validates.USERNAME_MAX_LEN:
            raise BadRequestError(
                "Bad username length. "
                f"REQUIRED: greater than or equal to {Validates.USERNAME_MIN_LEN}, "
                f"less than {Validates.USERNAME_MAX_LEN} "
                f"(yours: {username_length})")

    @staticmethod
    def state(state):
        if state is None:
            raise BadRequestError(
                f"State is None. (yours: {state})")

        state_type = type(state)
        if state_type is not str:
            raise BadRequestError(
                "Bad state type. "
                f"REQUIRED: {str} (yours: {state_type})")

        if not state in Validates.STATE_ENUM:
            raise BadRequestError(
                "Bad state. "
                f"REQUIRED: strings of {', '.join(Validates.STATE_ENUM)} (yours: {state})")
