/*704. Binary Search
Given an array of integers nums which is sorted in ascending order, and an integer target,
write a function to search target in nums. If target exists, then return its index. Otherwise, return -1.
You must write an algorithm with O(log n) runtime complexity.
*/

package com.algorithms.array.leetcode;

public class BinarySearch {

    public static void printArray(int[] arr) {
        int n = arr.length;
        for (int i = 0; i < n; i++) {
            System.out.print(arr[i] + " ");
        }
        System.out.println();
    }

    public static int search(int[] nums, int target) {
        int n = nums.length;
        int low = 0, high = n-1;
        while(low <= high){
            int mid = (low + high)/2 ;
            if(nums[mid] == target) return mid;
            else if(nums[mid] < target){
                low = mid + 1;
            }
            else{
                high = mid -1;
            }
        }
        return -1;
    }



    public static void main(String[] args) {
        int[] arr = {1, 2, 3, 4, 5, 6};
        int result = search(arr,6);
        System.out.println("The target index in binary search is: " + result);


    }
}
