/*
 Navicat Premium Data Transfer

 Source Server         : zhyy
 Source Server Type    : MySQL
 Source Server Version : 80015
 Source Host           : localhost:3306
 Source Schema         : login_users

 Target Server Type    : MySQL
 Target Server Version : 80015
 File Encoding         : 65001

 Date: 09/02/2019 20:02:52
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for expert_info
-- ----------------------------
DROP TABLE IF EXISTS `expert_info`;
CREATE TABLE `expert_info`  (
  `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `hospital` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `department` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `skill` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `content` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `phone` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `link` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 46 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of expert_info
-- ----------------------------
INSERT INTO `expert_info` VALUES (1, 'zhao', 'dsfasdasd', 'dasdasd', 'asdasd', 'asdasd', '16565626727', 'asdasd');
INSERT INTO `expert_info` VALUES (2, '李木子', '协和医院', '肿瘤科', '肿瘤', '专治肿瘤病', '17789897654', 'www');
INSERT INTO `expert_info` VALUES (3, '赵东', '中日友好医院', '外科', '外科病', '专治外科病', '12356784567', 'www');
INSERT INTO `expert_info` VALUES (7, 'lifei11', '中日友好医院', '皮肤科', '皮肤病', '专治皮肤病', '110', 'www');
INSERT INTO `expert_info` VALUES (8, 'lifei11', '中日友好医院', '皮肤科', '皮肤病', '专治皮肤病', '110', 'www');
INSERT INTO `expert_info` VALUES (9, 'lifei11', '中日友好医院', '皮肤科', '皮肤病', '专治皮肤病', '110', 'www');
INSERT INTO `expert_info` VALUES (10, 'lifei11', '中日友好医院', '皮肤科', '皮肤病', '专治皮肤病', '110', 'www');
INSERT INTO `expert_info` VALUES (11, 'lifei11', '中日友好医院', '皮肤科', '皮肤病', '专治皮肤病', '110', 'www');
INSERT INTO `expert_info` VALUES (12, 'lifei11', '中日友好医院', '皮肤科', '皮肤病', '专治皮肤病', '110', 'www');
INSERT INTO `expert_info` VALUES (13, 'lifei11', '中日友好医院', '皮肤科', '皮肤病', '专治皮肤病', '110', 'www');
INSERT INTO `expert_info` VALUES (14, 'lifei11', '中日友好医院', '皮肤科', '皮肤病', '专治皮肤病', '110', 'www');
INSERT INTO `expert_info` VALUES (15, 'lifei11', '中日友好医院', '皮肤科', '皮肤病', '专治皮肤病', '110', 'www');
INSERT INTO `expert_info` VALUES (16, 'lifei11', '中日友好医院', '皮肤科', '皮肤病', '专治皮肤病', '110', 'www');
INSERT INTO `expert_info` VALUES (17, 'lifei11', '中日友好医院', '皮肤科', '皮肤病', '专治皮肤病', '110', 'www');
INSERT INTO `expert_info` VALUES (18, 'lifei11', '中日友好医院', '皮肤科', '皮肤病', '专治皮肤病', '110', 'www');
INSERT INTO `expert_info` VALUES (19, 'lifei11', '中日友好医院', '皮肤科', '皮肤病', '专治皮肤病', '110', 'www');
INSERT INTO `expert_info` VALUES (20, 'lifei11', '中日友好医院', '皮肤科', '皮肤病', '专治皮肤病', '110', 'www');
INSERT INTO `expert_info` VALUES (21, 'lifei11', '中日友好医院', '皮肤科', '皮肤病', '专治皮肤病', '110', 'www');
INSERT INTO `expert_info` VALUES (22, 'lifei11', '中日友好医院', '皮肤科', '皮肤病', '专治皮肤病', '110', 'www');
INSERT INTO `expert_info` VALUES (23, 'lifei11', '中日友好医院', '皮肤科', '皮肤病', '专治皮肤病', '110', 'www');
INSERT INTO `expert_info` VALUES (24, 'lifei11', '中日友好医院', '皮肤科', '皮肤病', '专治皮肤病', '110', 'www');
INSERT INTO `expert_info` VALUES (25, 'lifei11', '中日友好医院', '皮肤科', '皮肤病', '专治皮肤病', '110', 'www');
INSERT INTO `expert_info` VALUES (26, 'lifei11', '中日友好医院', '皮肤科', '皮肤病', '专治皮肤病', '110', 'www');
INSERT INTO `expert_info` VALUES (27, 'lifei11', '中日友好医院', '皮肤科', '皮肤病', '专治皮肤病', '110', 'www');
INSERT INTO `expert_info` VALUES (28, 'lifei11', '中日友好医院', '皮肤科', '皮肤病', '专治皮肤病', '110', 'www');
INSERT INTO `expert_info` VALUES (29, 'lifei11', '中日友好医院', '皮肤科', '皮肤病', '专治皮肤病', '110', 'www');
INSERT INTO `expert_info` VALUES (30, 'lifei11', '中日友好医院', '皮肤科', '皮肤病', '专治皮肤病', '110', 'www');
INSERT INTO `expert_info` VALUES (31, 'lifei11', '中日友好医院', '皮肤科', '皮肤病', '专治皮肤病', '110', 'www');
INSERT INTO `expert_info` VALUES (32, 'lifei11', '中日友好医院', '皮肤科', '皮肤病', '专治皮肤病', '110', 'www');
INSERT INTO `expert_info` VALUES (33, 'lifei11', '中日友好医院', '皮肤科', '皮肤病', '专治皮肤病', '110', 'www');
INSERT INTO `expert_info` VALUES (34, 'lifei11', '中日友好医院', '皮肤科', '皮肤病', '专治皮肤病', '110', 'www');
INSERT INTO `expert_info` VALUES (35, 'lifei11', '中日友好医院', '皮肤科', '皮肤病', '专治皮肤病', '110', 'www');
INSERT INTO `expert_info` VALUES (36, 'lifei11', '中日友好医院', '皮肤科', '皮肤病', '专治皮肤病', '110', 'www');
INSERT INTO `expert_info` VALUES (37, 'lifei11', '中日友好医院', '皮肤科', '皮肤病', '专治皮肤病', '110', 'www');
INSERT INTO `expert_info` VALUES (38, 'lifei11', '中日友好医院', '皮肤科', '皮肤病', '专治皮肤病', '110', 'www');
INSERT INTO `expert_info` VALUES (39, 'lifei11', '中日友好医院', '皮肤科', '皮肤病', '专治皮肤病', '110', 'www');
INSERT INTO `expert_info` VALUES (40, 'lifei11', '中日友好医院', '皮肤科', '皮肤病', '专治皮肤病', '110', 'www');
INSERT INTO `expert_info` VALUES (41, 'lifei11', '中日友好医院', '皮肤科', '皮肤病', '专治皮肤病', '110', 'www');
INSERT INTO `expert_info` VALUES (42, 'lifei11', '中日友好医院', '皮肤科', '皮肤病', '专治皮肤病', '110', 'www');
INSERT INTO `expert_info` VALUES (44, 'sadjasbbcxzn', 'dasjdhas', 'asdasd', 'zbczhzcjsad', 'wqyeuqwyeu', '12312323', 'jdfhjdmsdasadk');
INSERT INTO `expert_info` VALUES (45, '王亚红', 'sada', 'asdas', 'zxczx', 'sadas', 'asdas', 'asdasasddasd');
INSERT INTO `expert_info` VALUES (46, '王益', 'dsada', 'dasd', 'zvz', 'dasd', '18844549878', 'dsf');

SET FOREIGN_KEY_CHECKS = 1;
