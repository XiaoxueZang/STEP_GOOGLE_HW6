/******************************************************************************

                      ==========================================
        Network:      Boltzmann Machine with Simulated Annealing
                      ==========================================

        Application:  Optimization
                      Traveling Salesman Problem

        Author:       Karsten Kutza
        Date:         21.2.96

        Reference:    D.H. Ackley, G.E. Hinton, T.J. Sejnowski
                      A Learning Algorithm for Boltzmann Machines
                      Cognitive Science, 9, pp. 147-169, 1985

 ******************************************************************************/




/******************************************************************************
                            D E C L A R A T I O N S
 ******************************************************************************/


#include <stdlib.h>
#include <stdio.h>
#include <math.h>


typedef int           BOOL;
typedef int           INT;
typedef double        REAL;

#define FALSE         0
#define TRUE          1
#define NOT           !
#define AND           &&
#define OR            ||

#define PI            (2*asin(1))
#define sqr(x)        ((x)*(x))

typedef struct {                     /* A NET:                                */
        INT           Units;         /* - number of units in this net         */
        BOOL*         Output;        /* - output of ith unit                  */
        INT*          On;            /* - counting on states in equilibrium   */
        INT*          Off;           /* - counting off states in equilibrium  */
        REAL*         Threshold;     /* - threshold of ith unit               */
        REAL**        Weight;        /* - connection weights to ith unit      */
        REAL          Temperature;   /* - actual temperature                  */
} NET;


/******************************************************************************
        R A N D O M S   D R A W N   F R O M   D I S T R I B U T I O N S
 ******************************************************************************/


void InitializeRandoms()
{
  srand(4711);
}


BOOL RandomEqualBOOL()
{
  return rand() % 2;
}


INT RandomEqualINT(INT Low, INT High)
{
  return rand() % (High-Low+1) + Low;
}


REAL RandomEqualREAL(REAL Low, REAL High)
{
  return ((REAL) rand() / RAND_MAX) * (High-Low) + Low;
}


/******************************************************************************
               A P P L I C A T I O N - S P E C I F I C   C O D E
 ******************************************************************************/


int NUM_CITIES;
int N;//             (NUM_CITIES * NUM_CITIES)

REAL                  Gamma;
REAL                  Distance[2500][2500];

FILE*                 f;


void InitializeApplication(NET* Net, double* xVal, double* yVal)
{
  INT  n1,n2;
  REAL x1,x2,y1,y2;
  REAL Alpha1, Alpha2;

  Gamma = 3100;
  for (n1=0; n1<NUM_CITIES; n1++) {
    for (n2=0; n2<NUM_CITIES; n2++) {
      //Alpha1 = ((REAL) n1 / NUM_CITIES) * 2 * PI;
      //Alpha2 = ((REAL) n2 / NUM_CITIES) * 2 * PI;
      x1 = *(xVal+n1);
      y1 = *(yVal+n1);
      x2 = *(xVal+n2);
      y2 = *(yVal+n2);
      Distance[n1][n2] = sqrt(sqr(x1-x2) + sqr(y1-y2));
    }
  }
  f = fopen("BOLTZMAN.txt", "w");
  fprintf(f, "Temperature    Valid    Length    Tour\n\n");
}


void CalculateWeights(NET* Net)
{
  INT  n1,n2,n3,n4;
  INT  i,j;
  INT  Pred_n3, Succ_n3;
  REAL Weight;

  for (n1=0; n1<NUM_CITIES; n1++) {
    for (n2=0; n2<NUM_CITIES; n2++) {
      i = n1*NUM_CITIES+n2;
      for (n3=0; n3<NUM_CITIES; n3++) {
        for (n4=0; n4<NUM_CITIES; n4++) {
          j = n3*NUM_CITIES+n4;
          Weight = 0;
          if (i!=j) {
            Pred_n3 = (n3==0 ? NUM_CITIES-1 : n3-1);
            Succ_n3 = (n3==NUM_CITIES-1 ? 0 : n3+1);
            if ((n1==n3) OR (n2==n4))
              Weight = -Gamma;
            else if ((n1 == Pred_n3) OR (n1 == Succ_n3))
              Weight = -Distance[n2][n4];
          }
          Net->Weight[i][j] = Weight;
        }
      }
      Net->Threshold[i] = -Gamma/2;
    }
  }
}


BOOL ValidTour(NET* Net)
{
  INT n1,n2;
  INT Cities, Stops;

  for (n1=0; n1<NUM_CITIES; n1++) {
    Cities = 0;
    Stops  = 0;
    for (n2=0; n2<NUM_CITIES; n2++) {
      if (Net->Output[n1*NUM_CITIES+n2]) {
        if (++Cities > 1)
          return FALSE;
      }
      if (Net->Output[n2*NUM_CITIES+n1]) {
        if (++Stops > 1)
          return FALSE;
      }
    }
    if ((Cities != 1) OR (Stops != 1))
      return FALSE;
  }
  return TRUE;
}


REAL LengthOfTour(NET* Net)
{
  INT  n1,n2,n3;
  REAL Length;

  Length = 0;
  for (n1=0; n1<NUM_CITIES; n1++) {
    for (n2=0; n2<NUM_CITIES; n2++) {
      if (Net->Output[((n1) % NUM_CITIES)*NUM_CITIES+n2])
        break;
    }
    for (n3=0; n3<NUM_CITIES; n3++) {
      if (Net->Output[((n1+1) % NUM_CITIES)*NUM_CITIES+n3])
        break;
    }
    Length += Distance[n2][n3];
  }
  return Length;
}


void WriteTour(NET* Net)
{
  INT  n1,n2;
  BOOL First;

  if (ValidTour(Net))
    fprintf(f, "%11.6f      yes    %6.3f    ", Net->Temperature, LengthOfTour(Net));
  else
    fprintf(f, "%11.6f       no              ", Net->Temperature);

  for (n1=0; n1<NUM_CITIES; n1++) {
    First = TRUE;
    fprintf(f, "[");
    for (n2=0; n2<NUM_CITIES; n2++) {
      if (Net->Output[n1*NUM_CITIES+n2]) {
        if (First) {
          First = FALSE;
          fprintf(f, "%d", n2);
        }
        else {
          fprintf(f, ", %d", n2);
        }
      }
    }
    fprintf(f, "]");
    if (n1 != NUM_CITIES-1) {
      fprintf(f, " -> ");
    }
  }
  fprintf(f, "\n");
}


void FinalizeApplication(NET* Net)
{
  fclose(f);
}


/******************************************************************************
                          I N I T I A L I Z A T I O N
 ******************************************************************************/


void GenerateNetwork(NET* Net)
{
  INT i;

  Net->Units     = N;
  Net->Output    = (BOOL*)  calloc(N, sizeof(BOOL));
  Net->On        = (INT*)   calloc(N, sizeof(INT));
  Net->Off       = (INT*)   calloc(N, sizeof(INT));
  Net->Threshold = (REAL*)  calloc(N, sizeof(REAL));
  Net->Weight    = (REAL**) calloc(N, sizeof(REAL*));

  for (i=0; i<N; i++) {
    Net->Weight[i] = (REAL*) calloc(N, sizeof(REAL));
  }
}


void SetRandom(NET* Net)
{
  INT i;

  for (i=0; i<Net->Units; i++) {
    Net->Output[i] = RandomEqualBOOL();
  }
}


/******************************************************************************
                     P R O P A G A T I N G   S I G N A L S
 ******************************************************************************/


void PropagateUnit(NET* Net, INT i)
{
  INT  j;
  REAL Sum, Probability;

  Sum = 0;
  for (j=0; j<Net->Units; j++) {
    Sum += Net->Weight[i][j] * Net->Output[j];
  }
  Sum -= Net->Threshold[i];
  Probability = 1 / (1 + exp(-Sum / Net->Temperature));
  if (RandomEqualREAL(0, 1) <= Probability)
    Net->Output[i] = TRUE;
  else
    Net->Output[i] = FALSE;
}


/******************************************************************************
                      S I M U L A T I N G   T H E   N E T
 ******************************************************************************/


void BringToThermalEquilibrium(NET* Net)
{
  INT n,i;

  for (i=0; i<Net->Units; i++) {
    Net->On[i]  = 0;
    Net->Off[i] = 0;
  }

  for (n=0; n<1000*Net->Units; n++) {
    PropagateUnit(Net, i = RandomEqualINT(0, Net->Units-1));
  }
  for (n=0; n<100*Net->Units; n++) {
    PropagateUnit(Net, i = RandomEqualINT(0, Net->Units-1));
    if (Net->Output[i])
      Net->On[i]++;
    else
      Net->Off[i]++;
  }

  for (i=0; i<Net->Units; i++) {
    Net->Output[i] = Net->On[i] > Net->Off[i];
  }
}


void Anneal(NET* Net)
{
  Net->Temperature = 3000;
  do {
    BringToThermalEquilibrium(Net);
    WriteTour(Net);
    Net->Temperature *= 0.99;
  } while (NOT ValidTour(Net));
}


/******************************************************************************
                                    M A I N
 ******************************************************************************/

#define MAX_CITIES    2500

int main(int argc, char* argv[])
{
  NET Net;
  FILE *fp;
  char* index, *indexj;
  double xVal[MAX_CITIES];
  double yVal[MAX_CITIES];
  char *fname = argv[1];
  //printf("file name is %s\n", fname);
  fp = fopen( fname, "r" );
  if( fp == NULL ){
    printf( "%sファイルが開けません¥n", fname);
    return -1;
  }
  int i = 0;
  int ret;
  char buff[10];
  fscanf(fp, "%s", buff);

  while( ( ret = fscanf( fp, "%lf,%lf", xVal+i, yVal+i) ) != EOF ){
    printf( "%lf %lf\n", *(xVal+i), *(yVal+i));
    i++;
  }
  printf("i is %d\n",i);
  NUM_CITIES = i;
  N = (NUM_CITIES * NUM_CITIES);

  fclose( fp );

  InitializeRandoms();
  GenerateNetwork(&Net);
  InitializeApplication(&Net, xVal, yVal);
  CalculateWeights(&Net);
  SetRandom(&Net);
  Anneal(&Net);
  FinalizeApplication(&Net);
}

/*
Simulator Output for the Traveling Salesman Problem

Temperature    Valid    Length    Tour

 100.000000       no              []->[]->[]->[]->[]->[]->[]->[]->[]->[]
  99.000000       no              []->[]->[]->[]->[]->[]->[]->[]->[]->[]
  98.010000       no              []->[0]->[]->[]->[]->[]->[]->[]->[]->[]
  97.029900       no              []->[]->[]->[]->[]->[]->[]->[]->[]->[]
  96.059601       no              []->[]->[]->[]->[]->[]->[]->[]->[]->[]
  95.099005       no              []->[]->[]->[]->[]->[]->[]->[]->[]->[9]
  94.148015       no              []->[]->[]->[]->[5]->[]->[0]->[]->[]->[]
  93.206535       no              []->[]->[]->[]->[]->[]->[]->[9]->[]->[]
  92.274469       no              []->[]->[]->[]->[]->[]->[]->[]->[]->[]
  91.351725       no              []->[]->[]->[]->[]->[]->[]->[]->[]->[]
          .        .              .
          .        .              .
          .        .              .
   0.763958       no              [5]->[]->[]->[0]->[]->[]->[]->[]->[7]->[6]
   0.756318       no              []->[0]->[1]->[2]->[]->[8]->[7]->[6]->[5]->[3]
   0.748755       no              []->[]->[]->[]->[]->[]->[7]->[6]->[]->[]
   0.741268       no              []->[]->[]->[]->[]->[]->[]->[]->[]->[]
   0.733855       no              [0]->[]->[]->[]->[]->[]->[]->[2]->[]->[]
   0.726516       no              []->[2]->[3]->[]->[]->[]->[]->[]->[0]->[9]
   0.719251       no              []->[]->[]->[]->[]->[5]->[]->[]->[]->[]
   0.712059       no              []->[]->[]->[]->[]->[]->[]->[]->[7]->[]
   0.704938       no              []->[]->[]->[]->[8]->[]->[9]->[]->[]->[3]
   0.697889      yes     7.295    [8]->[9]->[0]->[1]->[2]->[3]->[5]->[4]->[6]->[7]
*/