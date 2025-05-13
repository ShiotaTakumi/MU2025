CXX = g++
CXXFLAGS = -std=c++17 -O2 -I/opt/homebrew/include
LDFLAGS = -L/opt/homebrew/lib

TARGET = planar
SRC = planar.cpp

all: $(TARGET)

$(TARGET): $(SRC)
	$(CXX) $(CXXFLAGS) $(SRC) -o $(TARGET) $(LDFLAGS)

clean:
	rm -f $(TARGET)
