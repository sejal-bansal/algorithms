package com.algorithms.search;
//https://leetcode.com/problems/find-numbers-with-even-number-of-digits/
public class LCEvenNumOfDigits {
    public static void main(String[] args) {
        int[] nums = {10, 789, 7653, 9, 8, 67, 90};

        System.out.println(findNumber(nums));
    }

    static int findNumber(int[] arr){
        int count = 0;
        for(int num : arr){
            if(even(num))
                count++;
        }
        return count;
    }

    static boolean even(int num) {
        int numberOfDigits = digits(num);
        return numberOfDigits % 2 == 0;
    }

    static int digits(int num){
        if (num < 0)
            num = num * -1;
        return (int)(Math.log10(num)) + 1;
    }
}
