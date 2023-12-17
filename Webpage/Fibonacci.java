public class Fibonacci {

    public static void main(String[] args) {
        int n = 100;
        long[] fibSequence = new long[n];

        fibSequence[0] = 0;
        fibSequence[1] = 1;

        for (int i = 2; i < n; i++) {
            fibSequence[i] = fibSequence[i - 1] + fibSequence[i - 2];
        }

        for (long number : fibSequence) {
            System.out.println(number);
        }
    }
}