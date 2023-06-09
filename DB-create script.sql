CREATE DATABASE [Testik]
GO

USE [Testik]
GO

CREATE TABLE [dbo].[BonusCard](
	[Number] [int] IDENTITY(1,1) NOT NULL,
	[Bonus] [int] NULL,
	[Type] [nvarchar](20) NULL,
	CONSTRAINT [PK_BonusCard] PRIMARY KEY CLUSTERED ([Number] ASC)
)
GO

ALTER TABLE [dbo].[BonusCard] ADD  CONSTRAINT [DF_BonusCard_Bonus]  DEFAULT ((0)) FOR [Bonus]
GO

ALTER TABLE [dbo].[BonusCard] ADD  CONSTRAINT [DF_BonusCard_Type]  DEFAULT (N'Стандартная') FOR [Type]
GO

CREATE TABLE [dbo].[Buyer](
	[Id] [int] IDENTITY(1,1) NOT NULL,
	[Email] [nvarchar](100) NOT NULL,
	[PhoneNumber] [nchar](12) NOT NULL,
	[FullName] [nvarchar](100) NOT NULL,
	[Login] [varchar](50) NOT NULL,
	[Password] [varchar](70) NOT NULL,
	[Address] [nvarchar](200) NULL,
	[Balance] [money] NOT NULL,
	[BonusCardNumber] [int] NULL,
 CONSTRAINT [PK_Buyer] PRIMARY KEY CLUSTERED ([Id] ASC),
 CONSTRAINT [Email(Unique)] UNIQUE NONCLUSTERED ([Email] ASC),
 CONSTRAINT [Login(Unique)] UNIQUE NONCLUSTERED ([Login] ASC),
 CONSTRAINT [PhoneNumber(Unique)] UNIQUE NONCLUSTERED ([PhoneNumber] ASC)
)
GO

ALTER TABLE [dbo].[Buyer] ADD CONSTRAINT [DF_Buyer_Balance]  DEFAULT ((0)) FOR [Balance]
GO

ALTER TABLE [dbo].[Buyer] ADD  CONSTRAINT [FK_Buyer_BonusCard] FOREIGN KEY([BonusCardNumber])
REFERENCES [dbo].[BonusCard] ([Number])
GO

CREATE TABLE [dbo].[JobTitle](
	[Id] [int] IDENTITY(1,1) NOT NULL,
	[Title] [nvarchar](50) NOT NULL,
	[Responsibilities] [text] NOT NULL,
 CONSTRAINT [PK_JobTitle] PRIMARY KEY CLUSTERED ([Id] ASC)
)
GO

CREATE TABLE [dbo].[OfflineStore](
	[Id] [int] IDENTITY(1,1) NOT NULL,
	[Address] [nvarchar](100) NOT NULL,
	[OpeningTime] [time](0) NOT NULL,
	[ClosingTime] [time](0) NOT NULL,
 CONSTRAINT [PK_OfflineStore] PRIMARY KEY CLUSTERED ([Id] ASC)
)
GO

CREATE TABLE [dbo].[Personal](
	[Id] [int] IDENTITY(1,1) NOT NULL,
	[FullName] [nvarchar](100) NOT NULL,
	[PhoneNumber] [nchar](12) NOT NULL,
	[Email] [nvarchar](100) NOT NULL,
	[Salary] [money] NOT NULL,
	[OfflineStore] [int] NOT NULL,
	[JobTitle] [int] NOT NULL,
 CONSTRAINT [PK_Personal] PRIMARY KEY CLUSTERED ([Id] ASC)
)
GO

ALTER TABLE [dbo].[Personal] ADD  CONSTRAINT [DF_Personal_Salary]  DEFAULT ((0)) FOR [Salary]
GO

ALTER TABLE [dbo].[Personal] ADD CONSTRAINT [FK_Personal_JobTitle] FOREIGN KEY([JobTitle])
REFERENCES [dbo].[JobTitle] ([Id])
GO

ALTER TABLE [dbo].[Personal] ADD  CONSTRAINT [FK_Personal_OfflineStore] FOREIGN KEY([OfflineStore])
REFERENCES [dbo].[OfflineStore] ([Id])
GO

CREATE TABLE [dbo].[Category](
	[Id] [int] IDENTITY(1,1) NOT NULL,
	[Title] [nvarchar](30) NULL,
	[Subcategory] [nvarchar](30) NULL,
 CONSTRAINT [PK_Category] PRIMARY KEY CLUSTERED ([Id] ASC)
)
GO

CREATE TABLE [dbo].[Support](
	[Id] [int] IDENTITY(1,1) NOT NULL,
	[FullName] [nvarchar](100) NOT NULL,
	[Email] [nvarchar](100) NOT NULL,
	[PhoneNumber] [nchar](12) NOT NULL,
	[Salary] [money] NOT NULL,
	[Login] [nvarchar](50) NOT NULL,
	[Password] [nvarchar](50) NOT NULL,
 CONSTRAINT [PK_Support] PRIMARY KEY CLUSTERED ([Id] ASC),
 CONSTRAINT [SupportEmail(Unique)] UNIQUE NONCLUSTERED ([Email] ASC),
 CONSTRAINT [SupportLogin(Unique)] UNIQUE NONCLUSTERED ([Login] ASC),
 CONSTRAINT [SupportPhone] UNIQUE NONCLUSTERED ([PhoneNumber] ASC)
)
GO

ALTER TABLE [dbo].[Support] ADD CONSTRAINT [DF_Support_Salary]  DEFAULT ((0)) FOR [Salary]
GO

CREATE TABLE [dbo].[Producer](
	[Id] [int] IDENTITY(1,1) NOT NULL,
	[CompanyName] [nvarchar](50) NULL,
	[Address] [nvarchar](100) NULL,
	[Mail] [nvarchar](100) NULL,
 CONSTRAINT [PK_Producer] PRIMARY KEY CLUSTERED ([Id] ASC)
)
GO

CREATE TABLE [dbo].[Product](
	[Id] [int] IDENTITY(1,1) NOT NULL,
	[Title] [nvarchar](50) NULL,
	[Cost] [money] NULL,
	[Count] [int] NULL,
	[Size] [int] NULL,
	[Color] [nvarchar](50) NULL,
	[Category] [int] NULL,
	[Producer] [int] NULL,
	[ImageUrl] [nvarchar](256) NULL,
	[Support] [int] NULL,
 CONSTRAINT [PK_Product] PRIMARY KEY CLUSTERED ([Id] ASC)
)
GO

ALTER TABLE [dbo].[Product] ADD  CONSTRAINT [FK_Product_Category] FOREIGN KEY([Category])
REFERENCES [dbo].[Category] ([Id])
GO

ALTER TABLE [dbo].[Product] ADD  CONSTRAINT [FK_Product_Producer] FOREIGN KEY([Producer])
REFERENCES [dbo].[Producer] ([Id])
GO

ALTER TABLE [dbo].[Product] ADD  CONSTRAINT [FK_Product_Support] FOREIGN KEY([Support])
REFERENCES [dbo].[Support] ([Id])
GO

CREATE TABLE [dbo].[OfflineStoreProducts](
	[Id] [bigint] NOT NULL,
	[Product] [int] NOT NULL,
	[OfflineStore] [int] NOT NULL,
	[Count] [int] NOT NULL,
	CONSTRAINT [PK_OfflineStoreProducts] PRIMARY KEY CLUSTERED ([Id] ASC)
)
GO

ALTER TABLE [dbo].[OfflineStoreProducts] ADD CONSTRAINT [DF_OfflineStoreProducts_Count]  DEFAULT ((0)) FOR [Count]
GO

ALTER TABLE [dbo].[OfflineStoreProducts] ADD  CONSTRAINT [FK_OfflineStoreProducts_OfflineStore] FOREIGN KEY([OfflineStore])
REFERENCES [dbo].[OfflineStore] ([Id])
GO

ALTER TABLE [dbo].[OfflineStoreProducts] ADD  CONSTRAINT [FK_OfflineStoreProducts_Product] FOREIGN KEY([Product])
REFERENCES [dbo].[Product] ([Id])
GO

CREATE TABLE [dbo].[Cart](
	[Id] [bigint] NOT NULL,
	[Buyer] [int] NOT NULL,
	[Product] [int] NOT NULL,
	[Count] [int] NOT NULL,
 CONSTRAINT [PK_Cart] PRIMARY KEY CLUSTERED ([Id] ASC)
)
GO

ALTER TABLE [dbo].[Cart] ADD  CONSTRAINT [FK_Cart_Buyer] FOREIGN KEY([Buyer])
REFERENCES [dbo].[Buyer] ([Id])
GO

ALTER TABLE [dbo].[Cart] ADD  CONSTRAINT [FK_Cart_Product] FOREIGN KEY([Product])
REFERENCES [dbo].[Product] ([Id])
GO

CREATE TABLE [dbo].[Courier](
	[Id] [int] IDENTITY(1,1) NOT NULL,
	[Fullname] [nvarchar](100) NOT NULL,
	[Salary] [money] NOT NULL,
	[PhoneNumber] [nchar](12) NULL,
 CONSTRAINT [PK_dd] PRIMARY KEY CLUSTERED ([Id] ASC)
)
GO

CREATE TABLE [dbo].[Order](
	[Id] [int] IDENTITY(1,1) NOT NULL,
	[Count] [int] NOT NULL,
	[Product] [int] NOT NULL,
	[Buyer] [int] NOT NULL,
	[CostDelivery] [money] NULL,
	[Type] [nvarchar](20) NULL,
	[Courier] [int] NULL,
	[DeliveryDate] [date] NULL,
	[Retrieved] [bit] NULL,
	[CostProduct] [money] NULL,
	[Bonuses] [int] NULL,
	[Address] [nvarchar](200) NULL,
 CONSTRAINT [PK_Order] PRIMARY KEY CLUSTERED ([Id] ASC)
)
GO

ALTER TABLE [dbo].[Order] ADD  CONSTRAINT [DF_Order_Count]  DEFAULT ((0)) FOR [Count]
GO

ALTER TABLE [dbo].[Order] ADD  CONSTRAINT [FK_Order_Buyer] FOREIGN KEY([Buyer])
REFERENCES [dbo].[Buyer] ([Id])
GO

ALTER TABLE [dbo].[Order] ADD  CONSTRAINT [FK_Order_Courier] FOREIGN KEY([Courier])
REFERENCES [dbo].[Courier] ([Id])
GO

ALTER TABLE [dbo].[Order] ADD  CONSTRAINT [FK_Order_Product] FOREIGN KEY([Product])
REFERENCES [dbo].[Product] ([Id])
GO