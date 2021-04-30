# 自动签到

使用github Actions自动签到, 每日定时触发, 仓库被star时也会触发, 可通过自已加星之后再取消来测试任务运行.

fork本仓库并设置好Secret后即可自动签到.

## 仓库secret设置

在如下位置新增secret, 输入相应的名称与值即可.

![Secret位置](doc/img/secret_location.png)

## 需设置secret

### 几鸡

| secret名称       | 说明       |
| :-:              | :-:        |
| CHICKEN_MAIL     | 几鸡用户名 |
| CHICKEN_PASSWORD | 几鸡密码   |

### 爱桌游

| secret名称           | 说明         |
| :-:                  | :-:          |
| LOVEZHUOYOU_USER     | 爱桌游用户名 |
| LOVEZHUOYOU_PASSWORD | 爱桌游密码   |

