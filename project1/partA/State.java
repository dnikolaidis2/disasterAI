import java.util.*; 
import java.lang.Math; 

public class State implements Cloneable {

    private int [] position;
    private State parentNode = null;
    private Grid grid;
    private int numOfRows;
    private int numOfColumns;
    private double f=0, g=0, h=0;   

   

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
            if (!this.grid.getCell(this.position).isWall())
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
    
    public ArrayList<State> successorStates(boolean shuffle){

        ArrayList<State> childNodes = new ArrayList<State>();
        
        

        // Move Right. 
        int[] newPosition1 = new int[2]; 
        newPosition1[0] = this.position[0] + 1;
        newPosition1[1] = this.position[1];  

        State newState1 = new State(this.grid, newPosition1);  
        if (newState1.isLegal())
        {
            newState1.parentNode = this;
            newState1.generateF();
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
            newState2.generateF();
            childNodes.add(newState2);

                
        }

        // Move Up. 
        int[] newPosition3 = new int[2]; 
        newPosition3[0] = this.position[0];
        newPosition3[1] = this.position[1]+1;

        State newState3 = new State(this.grid, newPosition3);  
        if (newState3.isLegal())
        {
            newState3.parentNode = this;
            newState3.generateF();
            childNodes.add(newState3);
            
        }

        // Move Down.
        int[] newPosition4 = new int[2];  
        newPosition4[0] = this.position[0];
        newPosition4[1] = this.position[1]-1;

        State newState4 = new State(this.grid, newPosition4);  
        if (newState4.isLegal())
        {
            newState4.parentNode = this;
            newState4.generateF();
            childNodes.add(newState4);
                
        }

        if (shuffle) {
            Collections.shuffle(childNodes);
        }
        
        return childNodes; 
    }

    public double blockCost(){
        int[] grassIdxs = this.grid.getGrass();
        for(int i =0; i < grassIdxs.length; i++){
            if (this.getIdx() == grassIdxs[i])
                return this.grid.getGrassCost(); //Grass cost. 
        }
        return 1; //Terrain cost.  
    }
    
    public void generateF(){
        //Update g cost
        if (this.parentNode != null)
            this.g = this.parentNode.getG()+this.blockCost();

        //Find h
        this.h = findH();

        //Calculate f
        this.f = this.g + this.h; 
    }

    public double findH(){

        // We calculate our heuristic using the Euclidian Distance from our point to the end point
        double heur = Math.sqrt((Math.abs(this.position[0] - this.grid.getTerminal()[0]))^2 + 
                        (Math.abs(this.position[1] - this.grid.getTerminal()[1])^2));
        
        return heur; 
    }
    
    public int[] getPosition(){
        return this.position; 
    }

    public State getParentNode(){
        return this.parentNode;
    }

    public int getIdx(){
        return this.position[0]*grid.getNumOfColumns() + this.position[1];
    }

    public double getF(){
        return this.f;
    }

    public double getG(){
        return this.g; 
    }

    public void setG(double g){
        this.g = g; 
    }

    public Cell getCell() {
        return this.grid.getCell(this.position);
    }
}