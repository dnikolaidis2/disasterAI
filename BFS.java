import java.util.ArrayList;

import sun.awt.www.content.audio.x_aiff;

public class BFS {

    BFS(){}
    
    public void breadthFirstSearch(State initialState){
        int[] position = initialState.getPosition();
        int visitedStates[][] = new int[position[0]][position[1]];
        
        ArrayList<State> childNodes = initialState.successorStates();
        
    }

}