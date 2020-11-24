from chalice import BadRequestError

SUBJECT_MIN_LEN = 1
SUBJECT_MAX_LEN = 80
DESCRIPTION_MAX_LEN = 1000
USERNAME_MIN_LEN = 2
USERNAME_MAX_LEN = 128
STATE_ENUM = ["unstarted", "started", "completed"]


def subject(subject):
    if subject is None:
        raise BadRequestError(
            f"Subject is None. (You are: {None})")

    subject_type = type(subject)
    if subject_type is not str:
        raise BadRequestError(
            "Bad subject type. "
            f"REQUIRED: {str} (You are: {subject_type})")

    subject_length = len(subject)
    if not SUBJECT_MIN_LEN <= subject_length <= SUBJECT_MAX_LEN:
        raise BadRequestError(
            "Bad subject length. "
            f"REQUIRED: greater than or equal to {SUBJECT_MIN_LEN}, "
            f"less than or equal to {SUBJECT_MAX_LEN} "
            f"(You are: {subject_length})")


def description(description):
    description_type = type(description)
    if description_type is not str:
        raise BadRequestError(
            "Bad description type. "
            f"REQUIRED: {str} (You are: {description_type})")

    description_length = len(description)
    if not description_length <= DESCRIPTION_MAX_LEN:
        raise BadRequestError(
            "Bad subject length. "
            f"REQUIRED: less than or equal to {DESCRIPTION_MAX_LEN} "
            f"(You are: {description_length})")


def username(username):
    if username is None:
        raise BadRequestError(
            f"Username is None. (You are: {None})")

    username_type = type(username)
    if username_type is not str:
        raise BadRequestError(
            "Bad username type. "
            f"REQUIRED: {str} (You are: {username_type})")

    username_length = len(username)
    if not USERNAME_MIN_LEN <= username_length <= USERNAME_MAX_LEN:
        raise BadRequestError(
            "Bad username length. "
            f"REQUIRED: greater than or equal to {USERNAME_MIN_LEN}, "
            f"less than {USERNAME_MAX_LEN} "
            f"(You are: {username_length})")


def state(state):
    if state is None:
        raise BadRequestError(
            f"State is None. (You are: {state})")

    state_type = type(state)
    if state_type is not str:
        raise BadRequestError(
            "Bad state type. "
            f"REQUIRED: {str} (You are: {state_type})")

    if not state in STATE_ENUM:
        raise BadRequestError(
            "Bad state. "
            f"REQUIRED: strings of {', '.join(STATE_ENUM)} (You are: {state})")


def metadata(metadata):
    if metadata is None:
        raise BadRequestError(
            f"Metadata is None. (You are: {metadata})")

    # metadata_type = type(metadata)
    # if not isinstance(metadata, dict):
    #     raise BadRequestError(
    #         "Bad metadata type. "
    #         f"REQUIRED: {dict} (You are: {metadata_type})")
