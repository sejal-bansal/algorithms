package com.algorithms.search;

import java.util.Arrays;

public class SearchIn2DArray {
    public static void main(String[] args) {
        int[][] arr = {
                {10, 7, 4},
                {34, 78, 6, 98, 2},
                {4, 5, 8}
        };
        int target = 8;
        int[] ans = search2D(arr,target);
        System.out.println(Arrays.toString(ans));
        System.out.println(max2D(arr));
    }

    static int[] search2D(int[][] arr, int target){
        for(int row = 0; row < arr.length; row++){
            for(int col = 0; col < arr[row].length; col++){
                if(arr[row][col] == target)
                    return new int[]{row, col};
            }
        }
        return new int[]{-1, -1};
    }

    static int max2D(int[][] arr){
        int max = Integer.MIN_VALUE;
        for (int[] ints : arr) {
            for (int element : ints) {
                if (element > max)
                    max = element;
            }
        }
        return max;
    }
}
