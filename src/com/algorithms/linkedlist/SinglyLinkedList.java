package com.algorithms.linkedlist;

import java.util.LinkedList;

public class SinglyLinkedList {

    private LinkedList head;

    public static class ListNode{
        private int data;
        private ListNode next;

        public ListNode(int data){
            this.data = data;
            this.next = null;
        }
    }
}
