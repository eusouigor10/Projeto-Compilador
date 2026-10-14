program TestesCondicionais {
    int x, y;
    bool ativo;

    x = 10;
    y = 20;
    ativo = true;

    if (ativo) {
        x = x + 1;
    } else {
        x = x - 1;
    }

    if (x < y) {
        y = y + 1;
    }

    if (ativo) {
        if (x <= y) {
            x = x * 2;
        } else {
            x = x / 2;
        }
    }
}
