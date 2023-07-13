package com.algorithms.search.binary;

//https://leetcode.com/problems/peak-index-in-a-mountain-array/
public class PeakIndexMountainArray {
    public static void main(String[] args) {

    }

    public int peakIndexInMountainArray(int[] arr) {
        int start = 0;
        int end = arr.length - 1;

        while (start < end) {
            int mid = start + (end - start) / 2;
            if (arr[mid] > arr[mid + 1]) {
                //You are in the decreasing part of the array
                //this may be the ans, but look at left
                //this is why end != mid + 1
                end = mid;
            } else {
                //You are in ascending part of array
                start = mid + 1; // because we know that mid + 1 element > than mid element
            }
        }
        //in the end, start = end and pointing to the largest number because of the above two checks
        //start and end are always trying ot find max element in the above two checks,
        //hence when they are pointing to just one element, that is max because that is what the checks say
        //more elaboration : at every point of time for start and end, they have the best possible answer till that time
        // and if we are saying that only one item is remaining, hence because of above line, that is the best possible answer
        return start;
    }


}
