#Help https://youtu.be/H37f_x4wAC0
def octant_longest_subsequence_count():
    import pandas as pd
    try:
        data=pd.read_excel("input_octant_longest_subsequence.xlsx")
    except FileNotFoundError:
        print("Incorrect file name")  
    else:

        ##############################
        #Creating the columns in the excel sheet
        data["Octant"]="" 
        data[""]=""
        data["count"]=""
        data["Longest Subsequence Length"]=""
        data["Count"]=""
        values=["+1","-1","+2","-2","+3","-3","+4","-4"]
        for i in range(0,8,1):
            data.at[i,"count"]=values[i]
        ##############################
        lastval=data.index[-1]  #To calculate the last index, when index starts from 0 

        ##############################################
        #The following lines of code would check the numbers in the 3 columns and determine the octant values
        #based on the conditional statements provided
        #Calculating the octant value follows the same logic as described in the explanatory video
        for i in range(0,lastval+1,1):
            u=data["U'=U-U Avg"][i]
            v=data["V'=V-V Avg"][i]
            w=data["W'=W-W Avg"][i]
            if u>0:
                if v>0:
                    if w>0:
                        
                        data.at[i,'Octant']="+1"
                    else:
                        
                        data.at[i,'Octant']="-1"
                else:
                    if w>0:
                        
                        data.at[i,'Octant']="+4"
                    else:
                        
                        data.at[i,'Octant']="-4"
            else:
                if v>0:
                    if w>0:
                        data.at[i,'Octant']="+2"
                    else:
                        data.at[i,'Octant']="-2"
                else:
                    if w>0:
                        data.at[i,'Octant']="+3"
                    else: 
                        data.at[i,'Octant']="-3"
        count=[0,0,0,0,0,0,0,0] #creating an empty array to store the counted values of consecutive occurrences
        large=[0,0,0,0,0,0,0,0] #creating another empty array to store the largest consecutively counted occurrences
        for i in range(0,lastval,1):
            if(data['Octant'][i]==data['Octant'][i+1]):
                for j in range(0,8,1):
                    if (data['Octant'][i]==values[j]):
                        count[j]+=1
                        pos=j
            else:
                if (count[pos]>large[pos]):
                    large[pos]=count[pos]   
                    count[pos]=0
                    #print(i)
                else:
                    large[pos]=large[pos]   
                    count[pos]=0          
                    
        
        for j in range(0,8,1):
            for i in range(0,lastval,1):
                if (data['Octant'][i]==values[j]):
                    large[j]+=1
                    break
        
        #code to count how many largest occurrences present for each octant value
        count2=[0,0,0,0,0,0,0,0]              
        for j in range(0,8,1):                   
            for i in range(0,lastval-large[j]+1,1):
                supercount=0
                for k in range(0,large[j],1):
                    if(data['Octant'][i+k]==values[j]):
                        supercount+=1
                if(supercount==large[j]):
                    count2[j]+=1
        #code to insert the final values to the excel sheet
        for i in range(0,8,1):
            data.at[i,"Longest Subsequence Length"]=large[i]
            data.at[i,"Count"]=count2[i]
        data.to_excel("output_octant_longest_subsequence.xlsx",index=False)




from platform import python_version
ver = python_version()

if ver == "3.8.10":
    print("Correct Version Installed")
else:
    print("Please install 3.8.10. Instruction are present in the GitHub Repo/Webmail. Url: https://pastebin.com/nvibxmjw")


octant_longest_subsequence_count()