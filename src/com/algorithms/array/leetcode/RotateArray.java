//189. Rotate Array
// Given an array, rotate the array to the right by k steps, where k is non-negative.
package com.algorithms.array.leetcode;

public class RotateArray {

    public void printArray(int[] arr) {
        int n = arr.length;
        for (int i = 0; i < n; i++) {
            System.out.print(arr[i] + " ");
        }
        System.out.println();
    }
    public void rotate(int[] nums, int k) {

        k%= nums.length;
        reverse(nums, 0, nums.length-1);
        reverse(nums,0, k-1);
        reverse(nums, k, nums.length-1);

    }
    public void reverse(int[] nums, int start, int end){
        while(start < end){
            int temp = nums[start];
            nums[start] = nums[end];
            nums[end] = temp;
            start++;
            end--;
        }
    }

    public void main(String[] args) {
        int[] arr = {1, 2, 4, 5, 6};
        rotate(arr,3);
    }
}

