package com.algorithms;

public class NaturalNumber {
    public static void main(String[] args){
        double now = System.currentTimeMillis();
        NaturalNumber test = new NaturalNumber();
        System.out.println("Sum of the natural number:" + test.findSum(9999));
        System.out.println("Time Taken: " + (System.currentTimeMillis() - now) + " milliseconds");

//        nn.findSum1(n);
    }

    public int findSum(int n) {
        return n * (n + 1) / 2;
    }

    public int findSum1(int n){
        int sum = 0;
        for(int i = 1; i <= n; i++){
            sum = sum + i;
        }
        return sum;
    }


}
