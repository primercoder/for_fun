#define _CRT_SECURE_NO_WARNINGS
#include<stdio.h>
#include<stdlib.h>
#include<Windows.h>

// 手搓2048小游戏

int a[5][5];			// 4x4数组
int empty[17][2];		// 空格位置
int empty_num;			// 空格数量
int score = 0;			// 得分
void init()				// 初始化数组为0
{
	for (int i = 0; i < 5; i++)
	{
		for (int j = 0; j < 5; j++)
		{
			a[i][j] = 0;
		}
	}
}
void print()			// 打印数组
{
	for (int i = 1; i <= 4; i++)
	{
		for (int j = 1; j <= 4; j++)
		{
			printf("%6d ", a[i][j]);
		}
		printf("\n\n");
	}
}
void calculate()		// 计算数组空格数量并存储相应位置
{
	empty_num = 0;
	for (int i = 1; i <= 4; i++)
	{
		for (int j = 1; j <= 4; j++)
		{
			if (a[i][j] == 0)
			{
				empty_num++;
				empty[empty_num][0] = i;
				empty[empty_num][1] = j;
			}
		}
	}
}
void random_produce()		// 在随机位置产生新的数字1
{
	int r = rand() % empty_num + 1;
	a[empty[r][0]][empty[r][1]] = rand() % 2 + 1;
}
int move(int n)				// 移动算法，返回移动是否有效
{
	int movable = 0;
	// 向上移动
	if (n == 8)
	{
		for (int j = 1; j <= 4; j++)	// 对四列进行相应判断
		{
			int i = 1;
			for (i = 1; i <= 4; i++)
			{
				if (a[i][j] != 0) break;
			}
			if ((i > 1 && i < 4) || (i == 4 && a[4][j] != 0)) movable = 1;
			if (i == 1)
			{
				if (a[2][j] == 0)
				{
					if (a[3][j] != 0 || a[4][j] != 0) movable = 1;
				}
				if (a[3][j] == 0)
				{
					if (a[4][j] != 0) movable = 1;
				}
			}
			int not_zero = 0;
			for (i = 1; i <= 4; i++)
			{
				if (a[i][j] != 0)
				{
					not_zero++;
					a[not_zero][j] = a[i][j];
					if (i != not_zero) a[i][j] = 0;
				}
			}
			for (i = 1; i <= 3; i++)
			{
				if (a[i][j] != 0 && a[i][j] == a[i + 1][j])
				{
					a[i][j] *= 2;
					a[i + 1][j] = 0;
					score += a[i][j];
					movable = 1;
				}
			}
			not_zero = 0;
			for (i = 1; i <= 4; i++)
			{
				if (a[i][j] != 0)
				{
					not_zero++;
					a[not_zero][j] = a[i][j];
					if (i != not_zero) a[i][j] = 0;
				}
			}
		}
	}

	//down
	if (n == 2)
	{
		for (int j = 1; j <= 4; j++)
		{
			int i = 4;
			for (i = 4; i >= 1; i--)
			{
				if (a[i][j] != 0) break;
			}
			if ((i > 1 && i < 4) || (i == 1 && a[1][j] != 0)) movable = 1;
			if (i == 4)
			{
				if (a[3][j] == 0)
				{
					if (a[2][j] != 0 || a[1][j] != 0) movable = 1;
				}
				if (a[2][j] == 0)
				{
					if (a[1][j] != 0) movable = 1;
				}
			}
			int not_zero = 0;
			for (i = 4; i >= 1; i--)
			{
				if (a[i][j] != 0)
				{
					not_zero++;
					a[5-not_zero][j] = a[i][j];
					if (i != 5-not_zero) a[i][j] = 0;
				}
			}
			for (i = 4; i >=2; i--)
			{
				if (a[i][j] != 0 && a[i][j] == a[i - 1][j])
				{
					a[i][j] *= 2;
					a[i - 1][j] = 0;
					score += a[i][j];
					movable = 1;
				}
			}
			not_zero = 0;
			for (i = 4; i >= 1; i--)
			{
				if (a[i][j] != 0)
				{
					not_zero++;
					a[5-not_zero][j] = a[i][j];
					if (i != 5-not_zero) a[i][j] = 0;
				}
			}
		}
	}

	//right
	if (n == 6)
	{
		for (int i = 1; i <= 4; i++)
		{
			int j = 4;
			for (j = 4; j >= 1; j--)
			{
				if (a[i][j] != 0) break;
			}
			if ((j > 1 && j < 4) || (j == 1 && a[i][1] != 0)) movable = 1;
			if (j == 4)
			{
				if (a[i][3] == 0)
				{
					if (a[i][2] != 0 || a[i][1] != 0) movable = 1;
				}
				if (a[i][2] == 0)
				{
					if (a[i][1] != 0) movable = 1;
				}
			}
			int not_zero = 0;
			for (j = 4; j >= 1; j--)
			{
				if (a[i][j] != 0)
				{
					not_zero++;
					a[i][5-not_zero] = a[i][j];
					if (j != 5 - not_zero) a[i][j] = 0;
				}
			}
			for (j = 4; j >= 2; j--)
			{
				if (a[i][j] != 0 && a[i][j] == a[i][j-1])
				{
					a[i][j] *= 2;
					a[i][j-1] = 0;
					score += a[i][j];
					movable = 1;
				}
			}
			not_zero = 0;
			for (j = 4; j >= 1; j--)
			{
				if (a[i][j] != 0)
				{
					not_zero++;
					a[i][5-not_zero] = a[i][j];
					if (j != 5 - not_zero) a[i][j] = 0;
				}
			}
		}
	}

	//left
	if (n == 4)
	{
		for (int i = 1; i <= 4; i++)
		{
			int j = 1;
			for (j = 1; j <= 4; j++)
			{
				if (a[i][j] != 0) break;
			}
			if ((j > 1 && j < 4) || (j == 4 && a[i][4] != 0)) movable = 1;
			if (j == 1)
			{
				if (a[i][2] == 0)
				{
					if (a[i][3] != 0 || a[i][4] != 0) movable = 1;
				}
				if (a[i][3] == 0)
				{
					if (a[i][4] != 0) movable = 1;
				}
			}
			int not_zero = 0;
			for (j = 1; j <= 4; j++)
			{
				if (a[i][j] != 0)
				{
					not_zero++;
					a[i][not_zero] = a[i][j];
					if (j != not_zero) a[i][j] = 0;
				}
			}
			for (j = 1; j <= 3; j++)
			{
				if (a[i][j] != 0 && a[i][j] == a[i][j+1])
				{
					a[i][j] *= 2;
					a[i][j + 1] = 0;
					score += a[i][j];
					movable = 1;
				}
			}
			not_zero = 0;
			for (j = 1; j <= 4; j++)
			{
				if (a[i][j] != 0)
				{
					not_zero++;
					a[i][not_zero] = a[i][j];
					if (j != not_zero) a[i][j] = 0;
				}
			}
		}
	}
	return movable;
}
int ismovable(int n)		//判断是否可以移动
{
	// 向上移动
	if (n == 8)
	{
		for (int j = 1; j <= 4; j++)	// 对四列进行相应判断
		{
			int i = 1;
			for (i = 1; i <= 4; i++)
			{
				if (a[i][j] != 0) break;
			}
			if ((i > 1 && i < 4) || (i == 4 && a[4][j] != 0)) return 1;
			if (i == 1)
			{
				if (a[2][j] == 0)
				{
					if (a[3][j] != 0 || a[4][j] != 0) return 1;
				}
				if (a[3][j] == 0)
				{
					if (a[4][j] != 0) return 1;
				}
			}
			for (i = 1; i <= 3; i++)
			{
				if (a[i][j] != 0 && a[i][j] == a[i + 1][j]) return 1;
			}
		}
		return 0;
	}

	//down
	if (n == 2)
	{
		for (int j = 1; j <= 4; j++)
		{
			int i = 4;
			for (i = 4; i >= 1; i--)
			{
				if (a[i][j] != 0) break;
			}
			if ((i > 1 && i < 4) || (i == 1 && a[1][j] != 0)) return 1;
			if (i == 4)
			{
				if (a[3][j] == 0)
				{
					if (a[2][j] != 0 || a[1][j] != 0) return 1;
				}
				if (a[2][j] == 0)
				{
					if (a[1][j] != 0) return 1;
				}
			}
			for (i = 4; i >= 2; i--)
			{
				if (a[i][j] != 0 && a[i][j] == a[i - 1][j]) return 1;
			}
		}
		return 0;
	}

	//right
	if (n == 6)
	{
		for (int i = 1; i <= 4; i++)
		{
			int j = 4;
			for (j = 4; j >= 1; j--)
			{
				if (a[i][j] != 0) break;
			}
			if ((j > 1 && j < 4) || (j == 1 && a[i][1] != 0)) return 1;
			if (j == 4)
			{
				if (a[i][3] == 0)
				{
					if (a[i][2] != 0 || a[i][1] != 0) return 1;
				}
				if (a[i][2] == 0)
				{
					if (a[i][1] != 0) return 1;
				}
			}
			for (j = 4; j >= 2; j--)
			{
				if (a[i][j] != 0 && a[i][j] == a[i][j - 1]) return 1;
			}
		}
		return 0;
	}

	//left
	if (n == 4)
	{
		for (int i = 1; i <= 4; i++)
		{
			int j = 1;
			for (j = 1; j <= 4; j++)
			{
				if (a[i][j] != 0) break;
			}
			if ((j > 1 && j < 4) || (j == 4 && a[i][4] != 0)) return 1;
			if (j == 1)
			{
				if (a[i][2] == 0)
				{
					if (a[i][3] != 0 || a[i][4] != 0) return 1;
				}
				if (a[i][3] == 0)
				{
					if (a[i][4] != 0) return 1;
				}
			}
			for (j = 1; j <= 3; j++)
			{
				if (a[i][j] != 0 && a[i][j] == a[i][j + 1]) return 1;
			}
		}
		return 0;
	}
	return 0;
}
int main()
{
	int result = 1; // 移动是否有效的结果
	char way;       // 移动方向
	init();			// 初始化
	while (1)
	{
		calculate();
		if(result&&empty_num) random_produce();	// 如果上一次移动有效，则在新的随机位置产生新的数1
		print();						// 打印数组
		if (ismovable(8) || ismovable(2) || ismovable(4) || ismovable(6))
		{
			way = _getch();					// 获取新的位置输入  w,s,a,d
			printf("%c\n", way);
			if (way == 'w') result = move(8);
			else if (way == 's') result = move(2);
			else if (way == 'a') result = move(4);
			else if (way == 'd') result = move(6);
		}
		else break;
		if (!result) printf("无效移动!\n");
	}
	printf("Game Over\n\n");
	printf("Final Score:%d\n\n", score);
	printf("Enter any key to exit...\n");
	_getch();
	return 0;
}