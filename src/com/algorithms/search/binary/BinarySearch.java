package com.algorithms.search.binary;

public class BinarySearch {
    public static void main(String[] args) {
        int[] arr = {10, 11, 34, 37, 55, 57, 67, 78, 89, 90, 92};
        int target = 56;
        int ans = binarySearch(arr, target);
        System.out.println(ans);
    }

    //return the index, and return -1 if not found
    static int binarySearch(int[] arr, int target) {
        int start = 0;
        int end = arr.length - 1;

        while (start <= end) {
            int mid = start + (end - start) / 2;

            if (target < arr[mid])
                end = mid - 1;
            else if (target > arr[mid])
                start = mid + 1;
            else return mid;
        }
        return end;
    }
}
