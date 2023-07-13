package com.algorithms.array;

import java.util.Scanner;

public class Palindrome {

    public boolean isPalindrome(String word) {
        char[] charArray = word.toCharArray();
        int start = 0;
        int end = charArray.length - 1;
        while(start < end) {
            if (charArray[start] != charArray[end]) {
                return false;
            }
            start++;
            end--;
        }
        return true;
    }

    public static void main(String[] args) {
        Palindrome palindrome = new Palindrome();
        Scanner word = new Scanner(System.in);
        System.out.print("Enter the String: ");
        String username = word.next();
        if(palindrome.isPalindrome(username)){
            System.out.println("The string is Palindrome");
        }else{
            System.out.println("The string is not Palindrome");
        }
    }


}
