CC      = g++-14
CFLAGS  = -O3 -std=c++17 -Wno-attributes -I/opt/homebrew/Cellar/nauty/2.8.9/include/nauty
LDFLAGS = -L/opt/homebrew/lib -lnauty
TARGET  = a.out
SRCS    = main.cpp
OBJS    = $(SRCS:.cpp=.o)

all: $(TARGET)

$(TARGET): $(OBJS)
	$(CC) $(CFLAGS) -o $@ $^ $(LDFLAGS)

%.o: %.cpp
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f a.out $(OBJS) $(TARGET)
