import java.util.*;

public class BFS {

    BFS(){

    }

    public State breadthFirstSearch(Grid grid){
        State initialState = new State(grid, grid.getStart());
        int[] position = initialState.getPosition();
        int visitedStates[][] = new int[position[0]+1][position[1]+1];

        Queue<State> queue = new LinkedList<>();
        queue.add(initialState);

        while (!queue.isEmpty()){

            State state = queue.remove(); 
            ArrayList<State> children = initialState.successorStates();
            
            if (state.goalReached())
                return state;


            while (!children.isEmpty()){
                State child = children.get(children.size()-1);
                if (!child.isVisited(visitedStates)){
                    queue.add(child);
                    System.out.println("child\n");
                }
                children.remove(child); 
            }
        }
        return null;
    }

}