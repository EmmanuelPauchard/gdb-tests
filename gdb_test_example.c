#include <stdio.h>
#include <stdint.h>

// gcc 'used' attribute makes sure the symbol is not optimized away
/**
 * Divide a by div, rounding to the nearest integer
 */
__attribute__((used)) uint32_t divide_and_round_to_nearest_int(uint32_t a, uint32_t div) {
  return (a + div/2) / div;
}

int main(int argc, char* argv[]) {
	printf("Hello, world");
}
