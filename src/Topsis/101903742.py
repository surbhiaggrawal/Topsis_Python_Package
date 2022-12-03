import sys
import pandas as pd 
import numpy as np

try:
    #raising exception if input parameters are not according to provided format
    if(len(sys.argv) != 5):
        raise Exception("Provide correct number of input parameters")

    #reading input from command line
    file = str(sys.argv[1])
    weights = str(sys.argv[2]).split(",")
    impacts = str(sys.argv[3]).split(",")

    #creating dataframe
    read_file = pd.read_excel(file)
    read_file.to_csv("101903759-data.csv", index = None, header = True)
    df = pd.read_csv("101903759-data.csv")
    df.head()

    #raising exception if input file has columns < 3
    if(len(list(df.columns)) < 3):
        raise Exception("Input file contains less number of columns")

    #Impacts must be either +ve or -ve
    for i in impacts:
        if(i not in ['+', '-']):
            raise Exception("Impacts must be either +ve or -ve")

    #Number of weights, number of impacts and number of columns (from 2nd to last columns) must be same.
    if(len(list(df.columns))-1 != len(weights) or len(weights) != len(impacts)):
        raise Exception("Number of weights, number of impacts and number of columns (from 2nd to last columns) must be same.")

   # columns must be numeric
    cols = list(df.columns[1:])
    for y in cols:
        if(df[y].dtype not in [np.float64, np.int64]):
            raise Exception("columns must be numeric")

    # Arguments are dataset, number of columns, and weights of each column 
    def Normalize(dataset, nCol, weights):
        for i in range(1, nCol):
            temp = 0
            # Calculating Root of Sum of squares of a particular column
            for j in range(len(dataset)):
                temp = temp + dataset.iloc[j, i]**2
            temp = temp**0.5
            # Weighted Normalizing a element
            for j in range(len(dataset)):
                dataset.iat[j, i] = (dataset.iloc[j, i] / temp)*weights[i-1]
        print(dataset)

    # Calculate ideal best and ideal worst
    def Calc_Values(dataset, nCol, impact):
        p_sln = (dataset.max().values)[1:]
        n_sln = (dataset.min().values)[1:]
        for i in range(1, nCol):
            if impact[i-1] == '-':
                p_sln[i-1], n_sln[i-1] = n_sln[i-1], p_sln[i-1]
        return p_sln, n_sln

    # Calculating positive and negative values
    nCol = len(list(df.columns))
    p_sln, n_sln = Calc_Values(df, nCol , impacts)

    # calculating topsis score
    score = [] # Topsis score
    pp = [] # distance positive
    nn = [] # distance negative
    
    # Calculating distances and Topsis score for each row
    for i in range(len(df)):
        temp_p, temp_n = 0, 0
        for j in range(1, nCol):
            temp_p = temp_p + (p_sln[j-1] - df.iloc[i, j])**2
            temp_n = temp_n + (n_sln[j-1] - df.iloc[i, j])**2
        temp_p, temp_n = temp_p**0.5, temp_n**0.5
        score.append(temp_n/(temp_p + temp_n))
        nn.append(temp_n)
        pp.append(temp_p)
        
    # Appending new columns in dataset   
    df['Topsis Score'] = score
    
    # calculating the rank according to topsis score
    df['Rank'] = (df['Topsis Score'].rank(method='max', ascending=False))
    df = df.astype({"Rank": int})

    #exporting 101903759-result.csv
    df.to_csv(str(sys.argv[4]), index = None)

#handling exceptions
except Exception as Argument:
    print(Argument)
