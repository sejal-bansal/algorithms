package com.algorithms.search.binary;

public class SortedMatrix {
    public static void main(String[] args) {

    }

    static int[] binarySearch(int[][] matrix, int row, int cStart, int cEnd, int target) {
        while (cStart <= cEnd) {
            int mid = cStart + (cEnd - cStart) / 2;
            if (matrix[row][mid] == target)
                return new int[]{row, mid};
            if (matrix[row][mid] < target)
                cStart = mid + 1;
            else
                cEnd = mid - 1;
        }
        return new int[]{-1, -1};
    }

    static int[] search(int[][] matrix, int target) {
        int rows = matrix.length;
        int col = matrix[0].length; //be cautious, matrix maybe empty

        if (rows == 1)
            return binarySearch(matrix, 0, 0, col - 1, target);

        int rStart = 0;
        int rEnd = rows - 1;
        int cMid = col / 2;
        //run the loops till 2 rows are remaining

        while (rStart < rEnd - 1) { //while this is true it will have more than two rows
            int mid = rStart + (rEnd - rStart) / 2;
            if (matrix[mid][cMid] == target)
                return new int[]{mid, cMid};

            if(matrix[mid][cMid] < target)
                rStart = mid;
            else
                rEnd = mid;
        }

        //now we have two rows remaining
        return new int[]{-1,-1};

    }
}
