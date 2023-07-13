package com.algorithms.search.binary;
//https://leetcode.com/problems/find-in-mountain-array/
public class MountainArrayHard {
    public static void main(String[] args) {

    }

    int search(int[] arr, int target) {
        int peak = peakIndexInMountainArray(arr);
        int firstTry = orderAgnostic(arr, target, 0, peak);
        if (firstTry != -1) {
            return firstTry;
        }
        //try to search in second half
        return orderAgnostic(arr, target, peak + 1, arr.length - 1);
    }

    public int peakIndexInMountainArray(int[] arr) {
        int start = 0;
        int end = arr.length - 1;

        while (start < end) {
            int mid = start + (end - start) / 2;
            if (arr[mid] > arr[mid + 1]) {
                end = mid;
            } else {
                //You are in ascending part of array
                start = mid + 1; // because we know that mid + 1 element > than mid element
            }
        }
        return start;
    }

    static int orderAgnostic(int[] arr, int target, int start, int end) {
        //find whether the arr is sorted in ascending or descending order
        boolean isAsc = arr[start] < arr[end];
        while (start <= end) {
            int mid = start + (end - start) / 2;

            if (arr[mid] == target)
                return mid;

            if (isAsc) {
                if (target < arr[mid])
                    end = mid - 1;
                else
                    start = start + 1;
            } else {
                if (target > arr[mid])
                    end = mid - 1;
                else
                    start = start + 1;
            }
        }
        return -1;
    }

}
