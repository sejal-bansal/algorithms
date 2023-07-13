package com.algorithms.array.leetcode;

public class SquaresOfSortedArray {
    public static void printArray(int[] arr) {
        int n = arr.length;
        for (int i = 0; i < n; i++) {
            System.out.print(arr[i] + " ");
        }
        System.out.println();
    }

    public static int[] sortedSquares(int[] nums) {
        int[] result = new int[nums.length];
        for(int i =0; i < nums.length; i++){
            nums[i] = nums[i] * nums[i];
        }

        int head = 0;
        int tail = nums.length - 1;

        for(int pos = nums.length-1; pos >=0; pos--){
            if(nums[head] > nums[tail]){
                result[pos] = nums[head];
                head++;
            }
            else{
                result[pos] = nums[tail];
                tail--;
            }
        }
        return result;
    }

    public static void main(String[] args) {
        int[] num = {-4,-1,0,3,10};
        printArray(num);
        sortedSquares(num);
        printArray(num);
    }
}
