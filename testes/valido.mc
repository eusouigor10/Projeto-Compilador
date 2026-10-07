program TesteLexico {

    int x, resultado123;
    bool maior;

    x = 10;
    resultado123 = x + 20 * 2;
    maior = x < resultado123;
    maior = x <= resultado123;
    maior = x > resultado123;
    maior = x >= resultado123;
    maior = x == resultado123;
    maior = x != resultado123;
    maior = true && false;
    maior = true || false;
    maior = !maior;
    x = -10;

    if (maior) {
        write(x, resultado123);
    } else {
        read(x, resultado123);
    }
}