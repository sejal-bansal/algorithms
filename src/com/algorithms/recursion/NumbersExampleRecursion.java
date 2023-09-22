package com.algorithms.recursion;

public class NumbersExampleRecursion {
    public static void main(String[] args) {
        print(1);
    }

    static void print(int n) {
        if (n == 5) {  //Base condition
            System.out.println(5);
            return;
        }
        System.out.println(n);
        //recursive call
        //If you are calling a function again and again, you can treat it as  a separate call in the stack
        print(n + 1);
    }

}
