/**
			INTELLIGENCE LAB
	course		: 	COMP 417 - Artificial Intelligence
	authors		:	A. Vogiatzis, N. Trigkas
	excercise	:	1st Programming
	term 		: 	Spring 2019-2020
	date 		:   March 2020
*/
import java.util.Random;
import javax.swing.*;
import java.awt.Graphics;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.Component;
import java.util.ArrayList;
import java.awt.Canvas;

class GridGenerator{
	public static void VisualizeGrid(String frame_name, int xPos, int yPos, int N, int M, int [] walls, int [] grass, int start_idx, int terminal_idx ){
		JFrame frame = new JFrame(frame_name);
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		Canvas canvas = new Drawing(N,M,walls,grass,start_idx,terminal_idx);
		canvas.setSize(M*30,N*30);
		frame.add(canvas);
		frame.pack();
		Dimension size = frame.getSize();
		frame.setLocation((int)(size.getWidth()*xPos), (int)(size.getHeight()*yPos));
		frame.setVisible(true);
	}
	public static void VisualizeGrid(String frame_name, int xPos, int yPos, int N, int M, int [] walls, int [] grass, int [] steps ,int start_idx, int terminal_idx ){
		JFrame frame = new JFrame(frame_name);
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		Canvas canvas = new Drawing(N,M,walls,grass, steps, start_idx,terminal_idx);
		canvas.setSize(M*30,N*30);
		frame.add(canvas);
		frame.pack();
		Dimension size = frame.getSize();
		frame.setLocation((int)(size.getWidth()*xPos), (int)(size.getHeight()*yPos));
		frame.setVisible(true);
	}

	public static void main(String[] args) {
		String frame = "Random World";
		Grid mygrid;
		if (args.length<1)
			mygrid = new Grid();
		else if (args[0].equals("-i")){
			mygrid = new Grid(args[1]);
			frame = args[1].split("/")[1];
		}else if (args[0].equals("-d")){
			mygrid = new Grid(Integer.parseInt(args[1]),Integer.parseInt(args[2]));
		}else{
			mygrid = new Grid("world_examples/default.world");
			frame = "default.world";
		}
		int N = mygrid.getNumOfRows();
		int M = mygrid.getNumOfColumns();
		VisualizeGrid(frame,0,0,N,M,mygrid.getWalls(),mygrid.getGrass(),mygrid.getStartidx(),mygrid.getTerminalidx());
		
		//Breadth First Search 
		BFS bfs = new BFS();
		State goalStateBFS = bfs.breadthFirstSearch(mygrid);
		System.out.println("\n\n--------Breadth First Search---------\n\n");
		VisualizeGrid("BFS",1,0,N,M,mygrid.getWalls(),mygrid.getGrass(),generateSteps(goalStateBFS),mygrid.getStartidx(),mygrid.getTerminalidx());
		
		//Depth First Search
		DFS dfs = new DFS();
		State goalStateDFS = dfs.depthFirstSearch(mygrid);
		System.out.println("\n\n--------Depth Fisrt Search---------\n\n");
		VisualizeGrid("DFS",2,0,N,M,mygrid.getWalls(),mygrid.getGrass(),generateSteps(goalStateDFS),mygrid.getStartidx(),mygrid.getTerminalidx());
		
		//AStar Search
		AStar astar = new AStar();
		State goalStateAStar = astar.aStarSearch(mygrid);
		System.out.println("\n\n--------ASTAR---------\n\n");
		VisualizeGrid("AStar",3,0,N,M,mygrid.getWalls(),mygrid.getGrass(),generateSteps(goalStateAStar),mygrid.getStartidx(),mygrid.getTerminalidx());

		//LRTAStar Search
		// LRTAStar lartastar = new LRTAStar();
		// State goalStateLRTAStar = lartastar.LRTAStarSearch(mygrid);
		// System.out.println("\n\n--------LRTAStar---------\n\n");
		// VisualizeGrid("LRTAStar",0,1,N,M,mygrid.getWalls(),mygrid.getGrass(),generateSteps(goalStateLRTAStar),mygrid.getStartidx(),mygrid.getTerminalidx());
	}

	public static int[] generateSteps(State state){
		int moves = 0;
		State tempState = state;  
		while (tempState.getParentNode() != null){
			moves++;
			tempState = tempState.getParentNode();
		}
		
		int[] steps = new int[moves];

		tempState = state;
		int count=moves-1;  
		while (tempState.getParentNode() != null){
			steps[count] = tempState.getIdx();
			System.out.println("Step cost: "+tempState.getF());
			count--; 
			tempState = tempState.getParentNode();
		}
		reverse(steps, count);
        return steps;
	}
	
	public static void reverse(int a[], int n) 
    { 
        int i, k, t; 
        for (i = 0; i < n / 2; i++) { 
            t = a[i]; 
            a[i] = a[n - i - 1]; 
            a[n - i - 1] = t; 
		} 
	}
		
}