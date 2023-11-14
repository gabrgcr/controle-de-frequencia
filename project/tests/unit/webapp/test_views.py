def test_login_page(client):
    """Tests the login page

    :param client: App for testing
    """

    rv = client.get("/")
    assert rv.status_code == 200
    assert 'Senha' in rv.data.decode('utf-8')


def test_login(client):
    """Tests the login page

    :param client: App for testing
    """

    rv = client.post("/", '{"username" : "test", "password" : "test"}')
    rv.status_code == 200


def test_login_fail(client):
    """Tests the login page

    :param client: App for testing
    """

    rv = client.post("/", '{"username" : "no", "password" : "no"}')
    rv.status_code == 401


def test_turma(client):
    """Tests the turma page

    :param client: App for testing
    """

    rv = client.get("/turma")
    # assert rv.status_code == 200
    # assert 'Turma' in rv.data.decode('utf-8')