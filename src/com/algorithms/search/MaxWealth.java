package com.algorithms.search;

import java.net.Inet4Address;

//https://leetcode.com/problems/richest-customer-wealth/
public class MaxWealth {
    public static void main(String[] args) {


    }

    static int maxWealth(int[][] accounts){
        //person -> row, account -> col
        int ans = Integer.MIN_VALUE;
        //When you start a new col, take a new sum for that row
        for(int person = 0; person < accounts.length; person++){
            int sum = 0;
            for(int account = 0; account < accounts[person].length; account++){
                sum += accounts[person][account];
            }
            //now we have sum of accounts of person, check with the overall ans
            if(sum > ans){
                ans = sum;
            }
        }
        return ans;
    }
}

