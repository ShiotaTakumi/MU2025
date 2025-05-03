#include <iostream>
#include <boost/version.hpp>

using namespace std;

int main() {
    cout << "Hello, Boost!" << endl;
    cout << "Boost version: " 
              << BOOST_VERSION / 100000     << "."  // major
              << BOOST_VERSION / 100 % 1000 << "."  // minor
              << BOOST_VERSION % 100                // patch
              << endl;
}
