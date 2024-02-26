#include <iostream>

int fibonacci(int n) {
    if (n <= 1)
        return n;
    return fibonacci(n - 1) + fibonacci(n - 2);
}

int main() {

    int num[] = {7, 15, 31};
    
    std::cout << "Fibonacci Series: ";
    for (int i = 0; i < 3; i++) {
        std::cout << fibonacci(num[i]) << " ";
    }

    return 0;
}

// Output
// Fibonacci Series: 13 610 1346269 