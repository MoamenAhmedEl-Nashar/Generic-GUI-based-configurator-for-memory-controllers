
 `define ITEM2

 

`timescale 1ns/10ps
 parameter d = 2;

`ifdef ITEM1
`include "param.v"
`endif

`ifdef ITEM2
`include "param.v"
`endif

`ifdef ITEM3
`include "param.v"
`endif

`ifdef ITEM4
`include "param.v"
`endif