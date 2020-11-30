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
                f"There is no subject (Your Request: {subject}) "
                f"REQUIRED: subject is required.")

        subject_type = type(subject)
        if subject_type is not str:
            raise BadRequestError(
                f"subject type (Your Request: {subject_type}) "
                f"REQUIRED: {str}")

        subject_length = len(subject)
        if not Validates.SUBJECT_MIN_LEN <= subject_length <= Validates.SUBJECT_MAX_LEN:
            raise BadRequestError(
                f"subject length (Your Request: {subject_length}) "
                f"REQUIRED: subject length is greater than or equal to {Validates.SUBJECT_MIN_LEN}, "
                f"less than or equal to {Validates.SUBJECT_MAX_LEN}")

    @staticmethod
    def description(description):
        if description is None:
            return

        description_type = type(description)
        if description_type is not str:
            raise BadRequestError(
                f"description type (Your Request: {description_type}) "
                f"REQUIRED: {str}")

        description_length = len(description)
        if not description_length <= Validates.DESCRIPTION_MAX_LEN:
            raise BadRequestError(
                f"subject length (Your Request: {description_length}) "
                f"REQUIRED: less than or equal to {Validates.DESCRIPTION_MAX_LEN}")

    @staticmethod
    def state(state):
        if state is None:
            raise BadRequestError(
                f"there is no state. (Your Request: {None}) "
                f"REQUIRED: state is required.")

        state_type = type(state)
        if state_type is not str:
            raise BadRequestError(
                f"state type (Your Request: {state_type}) "
                f"REQUIRED: {str}")

        if not state in Validates.STATE_ENUM:
            raise BadRequestError(
                f"state enum (Your Request: {state}) "
                f"REQUIRED: {', '.join(Validates.STATE_ENUM)}")

    @staticmethod
    def username(username):
        if username is None:
            raise BadRequestError(
                f"there is no username. (Your Request: {None}) "
                f"REQUIRED: state is required.")

        username_type = type(username)
        if username_type is not str:
            raise BadRequestError(
                f"username type (Your Request: {username_type}) "
                f"REQUIRED: {str}")

        username_length = len(username)
        if not Validates.USERNAME_MIN_LEN <= username_length <= Validates.USERNAME_MAX_LEN:
            raise BadRequestError(
                f"username length (Your Request: {username_length}) "
                f"REQUIRED: greater than or equal to {Validates.USERNAME_MIN_LEN}, "
                f"less than {Validates.USERNAME_MAX_LEN}")
