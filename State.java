import java.util.*; 

public class State implements Cloneable {

    private int [] position;
    private State parentNode;
    private Grid grid;
    private int numOfRows;
    private int numOfColumns;  

   

    State(Grid grid, int[] position) {

        this.position = position;
        this.grid = grid; 
        this.numOfRows = grid.getNumOfRows()-1;
        this.numOfColumns = grid.getNumOfColumns()-1;
    }

    public Object clone()throws CloneNotSupportedException{  
        return super.clone();  
    } 

    public boolean isLegal(){
        if (this.position[0] >= 0 && this.position[0] <= numOfRows && 
            this.position[1] >= 0 && this.position[1] <= numOfColumns)
            {
                return true; 
            }
        return false;     
    }

    public boolean isVisited(int[][] visitedStates){
        if (visitedStates[this.position[0]][this.position[1]] == 1){
            return true; 
        } 
        visitedStates[this.position[0]][this.position[1]] = 1; 
        return false; 
    }
    
    public boolean goalReached(){
        if (Arrays.equals(this.position, this.grid.getTerminal()))
            return true; 
        return false; 
    }

    public ArrayList<State> successorStates(){

        ArrayList<State> childNodes = new ArrayList<State>();
        
        try{

            // Move Right. 
            int[] newPosition1 = new int[2]; 
            newPosition1[0] = this.position[0] + 1;
            newPosition1[1] = this.position[1];

            State newState1 = new State(this.grid, newPosition1);  
            if (newState1.isLegal())
            {
                newState1.parentNode = this;
                childNodes.add(newState1);
             
            }

            // Move Left.  
            int[] newPosition2 = new int[2];
            newPosition2[0] = this.position[0] -1;
            newPosition2[1] = this.position[1];
    
            State newState2 = new State(this.grid, newPosition2);  
            if (newState2.isLegal())
            {
                newState2.parentNode = this;
                childNodes.add((State)newState2.clone());
                 
            }

            // Move Up. 
            int[] newPosition3 = new int[2]; 
            newPosition3[0] = this.position[0];
            newPosition3[1] = this.position[1]+1;

            State newState3 = new State(this.grid, newPosition3);  
            if (newState3.isLegal())
            {
                newState3.parentNode = this;
                childNodes.add((State)newState3.clone());
             
            }

            // Move Down.
            int[] newPosition4 = new int[2];  
            newPosition4[0] = this.position[0];
            newPosition4[1] = this.position[1]-1;

            State newState4 = new State(this.grid, newPosition4);  
            if (newState4.isLegal())
            {
                newState4.parentNode = this;
                childNodes.add((State)newState4.clone());
                 
            }

        }catch(CloneNotSupportedException c){}

        return childNodes; 
    }

  

    public int[] getPosition(){
        return this.position; 
    }
}