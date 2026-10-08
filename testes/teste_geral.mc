program TesteGeral {

    int x, y;
    bool ativo;

    x = 10;
    y = x + 20 * 2;
    ativo = x <= y && true || !false;

    read(x, y);
    write(x, y, ativo);

    if (ativo) {
        x = -y;
    } else {
        x = (x + 1) / 2;
    }

    x = 0;
}
