#include <iostream>

int fibonacci(int n) {
    if (n <= 1)
        return n;
    return fibonacci(n - 1) + fibonacci(n - 2);
}

int main() {

    int num;
    num = [7,15,31];
    
    std::cout << "Fibonacci Series: ";
    for (int i = 0; i < num; i++) {
        std::cout << fibonacci(i) << " ";
    }

    return 0;
}
