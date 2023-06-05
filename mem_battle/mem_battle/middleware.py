def session_mem_id(get_response):
    """Middleware to create list in session for mem_id
    to filter mems user have already seen"""

    def middleware(request):
        # request.session.flush()
        if 'mem_seen' not in request.session:
            request.session['mem_seen'] = []
        if 'until_retrieve' not in request.session:
            request.session['until_retrieve'] = []

        response = get_response(request)

        return response

    return middleware